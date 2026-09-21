# -*- coding: utf-8 -*-
"""CLI command: run-functional — execute all tests/functional tests.

Requirement mapping:
  - 2.1 Concurrency fixed at 20 (configurable via config.json concurrency, env override)
  - 2.2 Concurrency unit = test suite (e.g. acl as one suite)
  - 2.3 Before each suite, find an available env from CloudPods resource pool; create one if none
  - 2.4 If a VM in pool is unreachable (SSH fails), delete and recreate
  - 2.5 After suite completes, release env control (do not delete)
  - 2.6 After all suites complete, delete all VMs in the resource pool
  - 2.7 Results aggregated to reports/functional/<YYYY-MM-DD>/

Usage:
  cli.py run-functional [--config ...] [--suite acl] [--dry-run] [--no-cleanup]
"""
from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

from core.base import BaseCommand

logger = logging.getLogger("ci_cli.commands.run_functional")


class RunFunctionalCommand(BaseCommand):
    """Execute all functional tests (resource pool + concurrency + reporting)."""

    name = "run-functional"

    @property
    def repo_root(self) -> Path:
        return Path.cwd()

    def setup_parser(self, parser):
        parser.add_argument("--config", default=None,
                            help="Path to functional config file (default .github/scripts/functional/config.json)")
        parser.add_argument("--suite", default=None,
                            help="Only execute specified suites (comma-separated)")
        parser.add_argument("--dry-run", action="store_true",
                            help="Only discover suites and print plan, no env creation/execution")
        parser.add_argument("--no-cleanup", action="store_true",
                            help="Do not delete VMs in resource pool after execution")
        parser.add_argument("--keep-logs", action="store_true",
                            help="Keep full logs of each execution (written to reports dir)")

    def run(self, args) -> int:
        repo_root = Path.cwd()
        try:
            from functional.config import load_config
            from functional.discovery import discover_suites
            from functional.resource_pool import EnvPool
            from functional.executor import package_repo, upload_repo, run_suite_on_env, ensure_tar
            from functional.report import build_report
            from core.ssh import SSHClient
        except ImportError as exc:
            logger.error("missing dependency: %s", exc)
            return 1

        cfg = load_config()
        if args.config:
            cfg_path = Path(args.config)
            if cfg_path.exists():
                with open(cfg_path, encoding="utf-8") as f:
                    cfg.update(json.load(f))

        concurrency = int(cfg.get("concurrency", 20))
        env_prefix = cfg.get("env_prefix", "openruyi-func")
        reports_root = Path(cfg.get("reports_root", "reports/functional"))
        suite_include = cfg.get("suite_include") or []
        suite_exclude = cfg.get("suite_exclude") or []
        if args.suite:
            suite_include = [s.strip() for s in args.suite.split(",") if s.strip()]

        # 1. Discover test suites
        suites, errors = discover_suites(repo_root, cfg)
        if errors:
            logger.warning("[run-functional] discovery errors: %s", errors)
        if suite_include:
            suites = [s for s in suites if s.name in suite_include]
        if suite_exclude:
            suites = [s for s in suites if s.name not in suite_exclude]
        if not suites:
            logger.error("[run-functional] no test suites found")
            return 1

        logger.info("[run-functional] found %d suite(s), concurrency=%d, prefix=%s",
                    len(suites), concurrency, env_prefix)

        # 2. dry-run: print plan and exit
        if args.dry_run:
            print(json.dumps([s.to_dict() for s in suites], ensure_ascii=False, indent=2))
            return 0

        # 3. Package repo (once, shared across envs)
        logger.info("[run-functional] packaging repo ...")
        tarball = package_repo(repo_root, excludes=cfg.get("repo_archive_excludes"))
        logger.info("[run-functional] repo packaged: %s (%.1f MB)",
                    tarball, os.path.getsize(tarball) / 1024 / 1024)

        # 4. Initialize resource pool
        pool = EnvPool(cfg, repo_root)
        all_results: List[Dict] = []
        results_lock = threading.Lock()
        errors_by_suite: Dict[str, str] = {}

        def run_one(suite):
            """Execute a single test suite: acquire env -> upload -> execute -> release."""
            spec = get_suite_spec_for(cfg, suite)
            env = pool.acquire(suite.name, spec)
            if env is None:
                return {"suite": suite.name, "cases": [], "error": "no env available"}
            ssh = None
            try:
                # Prefer env's actual ports (pool/new both have qemu_ports),
                # fall back to spec/config qemu_ssh_port_base
                ports = env.get("qemu_ports") or []
                qemu_port = int(ports[0]) if ports else int(
                    spec.get("qemu_ssh_port_base",
                             cfg.get("qemu_ssh_port_base", 12055)))
                ssh_user = spec.get("qemu_ssh_user",
                                    cfg.get("qemu_ssh_user", "openruyi"))
                ssh_pw = spec.get("qemu_ssh_password",
                                  cfg.get("qemu_ssh_password", "openruyi"))
                ssh = SSHClient(env["host_ip"], qemu_port, ssh_user, ssh_pw)

                # Upload repo
                if not ensure_tar(ssh, ssh_pw):
                    raise RuntimeError("tar unavailable in QEMU")
                if not upload_repo(ssh, tarball, ssh_pw):
                    raise RuntimeError("repo upload failed")

                # Execute cases within the suite (tmt)
                cases = [c.to_dict() for c in suite.cases]
                timeout = int(cfg.get("case_timeout", 5400))
                res = run_suite_on_env(
                    ssh, ssh_pw,
                    suite_fmf_path=suite.fmf_path,
                    cases=cases,
                    suite_name=suite.name,
                    timeout=timeout,
                )
                return res
            except Exception as exc:  # noqa: BLE001
                logger.error("[run-functional] suite %s failed: %s", suite.name, exc)
                return {"suite": suite.name, "cases": [],
                        "error": str(exc)}
            finally:
                if ssh is not None:
                    ssh.close()
                # Release env (do not delete)
                pool.release(env["server_id"])

        # 5. Concurrent execution (by test suite)
        with ThreadPoolExecutor(max_workers=concurrency) as pool_exec:
            futures = {pool_exec.submit(run_one, s): s for s in suites}
            for fut in as_completed(futures):
                suite = futures[fut]
                try:
                    res = fut.result()
                    if res.get("error"):
                        errors_by_suite[suite.name] = res["error"]
                    with results_lock:
                        all_results.append(res)
                    logger.info("[run-functional] done suite=%s cases=%d",
                                suite.name, len(res.get("cases", [])))
                except Exception as exc:  # noqa: BLE001
                    errors_by_suite[suite.name] = str(exc)
                    with results_lock:
                        all_results.append({"suite": suite.name, "cases": [],
                                            "error": str(exc)})

        # 6. Unified cleanup (default: delete all envs used in this batch)
        if not args.no_cleanup:
            logger.info("[run-functional] cleanup all pool envs ...")
            deleted = pool.cleanup_all()
            logger.info("[run-functional] cleanup deleted %d env(s)", deleted)
        else:
            logger.info("[run-functional] --no-cleanup: keep %d env(s)",
                        len(pool._used_pool))

        # 7. Generate report
        logger.info("[run-functional] generating report ...")
        paths = build_report(all_results)
        logger.info("[run-functional] report written: %s",
                    ", ".join(str(p) for p in paths.values()))

        # 8. Print console summary
        from functional.report import summarize_results
        summary = summarize_results(all_results)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        if errors_by_suite:
            print("suites with errors:", json.dumps(errors_by_suite, ensure_ascii=False))

        # Exit code: failures or error suites -> 1
        if summary["fail"] > 0 or summary["error"] > 0 or errors_by_suite:
            return 1
        return 0


def get_suite_spec_for(cfg: Dict, suite) -> Dict:
    """Build env spec for a test suite (defaults + per-suite overrides)."""
    from functional.config import get_suite_spec
    return get_suite_spec(cfg, suite.name)
