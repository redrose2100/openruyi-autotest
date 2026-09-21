# -*- coding: utf-8 -*-
"""Functional test suite executor.

Execute all test cases for a single test suite (e.g. acl) in an acquired
environment (QEMU VM):

  1. Package the repo (excluding docs/.github/unittests etc.) and upload to env
  2. Prepare execution environment inside QEMU (tmt / beakerlib, reusing
     run_tests_in_qemu logic)
  3. Configure topology.env (pointing to local host)
  4. Execute the test suite via tmt (--name /tests/functional/pkgs/<suite>):
     - Suite-level test cases (the suite directory's own test.sh) as suite cases
     - Sub-test-cases test_* each executed separately
  5. Parse output to get each case's pass/fail/error/skip and feature point details

Reuses run_tests_in_qemu's: remote_prepare_env / remote_setup_topology /
run_tmt_tests (filtered by --name) / run_tests_direct (when tmt unavailable).
"""
from __future__ import annotations

import json
import logging
import os
import re
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.ssh import SSHClient

logger = logging.getLogger("ci_cli.functional.executor")

# Reuse run_tests_in_qemu's remote prep / execution functions
from commands.run_tests_in_qemu import (
    _setup_ruamel_pure_python,
    remote_prepare_env,
    remote_setup_topology,
    run_tests_direct,
)

_REMOTE_DIR = "/home/openruyi/openruyi-autotest"


def package_repo(repo_root: Path, excludes: Optional[List[str]] = None) -> str:
    """Package repo as tar.gz (excluding .git and irrelevant dirs), return temp file path."""
    fd, tmp = tempfile.mkstemp(suffix=".tar.gz")
    os.close(fd)

    base_excludes = [".git", "docs", ".github", "unittests"]
    if excludes:
        base_excludes = list(dict.fromkeys(base_excludes + list(excludes)))
    with tarfile.open(tmp, "w:gz") as tar:
        for child in sorted(repo_root.iterdir()):
            if child.name in base_excludes:
                continue
            tar.add(child, arcname=f"openruyi-autotest/{child.name}")
    return tmp


def _exec3(ssh: SSHClient, cmd: str, **kw):
    r = ssh.exec(cmd, **kw)
    return r.code, r.stdout, r.stderr


def ensure_tar(ssh: SSHClient, ssh_pw: str) -> bool:
    """Ensure tar is available in QEMU (minimal systems may lack it)."""
    ssh.exec(f"echo '{ssh_pw}' | sudo -S true")
    code, out, err = _exec3(ssh, "command -v tar", timeout=30)
    if code == 0:
        return True
    code, out, err = _exec3(ssh,
        f"echo '{ssh_pw}' | sudo -S dnf install -y "
        "--nogpgcheck --setopt=sslverify=0 tar gzip 2>&1 | tail -5",
        timeout=600)
    code, out, err = _exec3(ssh, "command -v tar", timeout=30)
    return code == 0


def upload_repo(ssh: SSHClient, tarball: str, ssh_pw: str) -> bool:
    """Upload and extract repo tarball to a fixed directory inside QEMU."""
    ssh.exec(f"rm -rf {_REMOTE_DIR}")
    ssh.exec("mkdir -p /home/openruyi")
    if not ssh.put_file(tarball, "/home/openruyi/repo.tar.gz"):
        logger.error("[exec] upload repo failed")
        return False
    code, out, err = _exec3(ssh,
        "cd /home/openruyi && tar xzf repo.tar.gz && rm -f repo.tar.gz",
        timeout=300)
    if code != 0:
        logger.error("[exec] extract failed: %s %s", out[-300:], err[-300:])
        return False
    return True


def run_suite_on_env(
    ssh: SSHClient,
    ssh_pw: str,
    suite_fmf_path: str,
    cases: List[Dict],
    suite_name: str,
    timeout: int = 5400,
) -> Dict:
    """Execute all test cases for a single test suite in the connected environment.

    suite_fmf_path: FMF path of the suite (/tests/functional/pkgs/acl)
    cases: list of dicts for all cases under the suite, each containing
           {"case", "fmf_path", "test_points", ...}

    Returns result dict:
      {
        "suite": suite_name,
        "cases": [{"case","fmf_path","status","test_points","fail_reason","output"}],
        "exec_mode": "tmt"|"direct"|"",
      }
    """
    result: Dict = {
        "suite": suite_name,
        "cases": [],
        "exec_mode": "",
        "error": None,
    }

    # 1. Prepare execution environment (tmt/beakerlib)
    exec_mode = remote_prepare_env(ssh, ssh_pw)
    if not exec_mode:
        result["error"] = "prepare env failed"
        logger.error("[exec] %s: prepare env failed", suite_name)
        return result
    result["exec_mode"] = exec_mode

    # 2. Configure topology.env (pointing to localhost)
    remote_setup_topology(ssh, ssh_pw, "127.0.0.1")

    case_fmf_paths = [c["fmf_path"] for c in cases]

    # 3. Execute: tmt or direct
    suite_results: List[Dict] = []
    try:
        if exec_mode == "tmt":
            suite_results = _run_tmt_suite(ssh, ssh_pw, suite_fmf_path,
                                           case_fmf_paths, timeout)
        else:
            suite_results = _run_direct_suite(ssh, ssh_pw, suite_fmf_path,
                                              case_fmf_paths, timeout)
    except Exception as exc:  # noqa: BLE001
        # A single case failure should not discard already-collected suite results:
        # log the exception and continue normalization
        logger.error("[exec] %s: suite execution raised, "
                     "keeping %d partial result(s): %s",
                     suite_name, len(suite_results), exc)
        result["error"] = f"partial: {exc}"

    # 4. Normalize results (fill in fail_reason / test_points)
    case_by_path = {c["fmf_path"]: c for c in cases}
    for r in suite_results:
        case = case_by_path.get(r["fmf_path"], {})
        item = {
            "case": case.get("case", r["fmf_path"].rsplit("/", 1)[-1]),
            "fmf_path": r["fmf_path"],
            "status": r["status"],
            "test_points": case.get("test_points", 0),
            "fail_reason": r.get("fail_reason", ""),
            "output": r.get("output", ""),
        }
        result["cases"].append(item)

    return result


def _run_tmt_suite(ssh: SSHClient, ssh_pw: str, suite_fmf_path: str,
                   case_fmf_paths: List[str], timeout: int) -> List[Dict]:
    """Execute the entire test suite via tmt (suite itself + all sub-cases)."""
    results: List[Dict] = []
    # tmt --name matches subtrees: passing the suite path covers all sub-cases
    cmd = (
        f"cd {_REMOTE_DIR} && "
        f"echo '{ssh_pw}' | sudo -S true && "
        f"timeout {timeout} tmt run --all plan --name /plans/functional "
        f"--name {suite_fmf_path} provision --feeling-safe 2>&1"
    )
    logger.info("[exec] %s: running tmt suite: %s...", suite_fmf_path, cmd[:300])
    code, out, err = _exec3(ssh, cmd, timeout=timeout + 60)
    output = out + ("\n[stderr]\n" + err if err else "")
    logger.info("[exec] %s: tmt exit=%s, output len=%s", suite_fmf_path, code,
                len(output))

    # Parse case statuses from tmt tree-style output
    parsed = _parse_tmt_output(output, case_fmf_paths)
    if parsed:
        return parsed

    # Parse failed: mark entire suite
    status = "fail" if (code != 0 or "fail" in output.lower()) else "pass"
    results.append({
        "fmf_path": suite_fmf_path,
        "status": status,
        "fail_reason": "tmt output unparsed" if status == "fail" else "",
        "output": output[-4000:],
    })
    return results


def _parse_tmt_output(output: str, case_fmf_paths: List[str]) -> List[Dict]:
    """Parse tmt tree-style output, returning results for each case."""
    results: List[Dict] = []
    lines = output.splitlines()
    current_test = None
    current_fail_reason: List[str] = []
    # Noise line prefixes (tmt stage headers etc.), exclude as non-failure reasons
    _NOISE = (
        "discover", "provision", "prepare", "execute", "report", "plan",
        "summary", "1 test", "total", "Result", "How", "finish",
    )
    pending_result: Optional[Dict] = None  # Parsed result awaiting failure detail capture
    for line in lines:
        m = re.match(r"^\s*(/tests/\S+)\s*$", line)
        if m:
            current_test = m.group(1)
            current_fail_reason = []
            pending_result = None
            continue
        if current_test:
            m2 = re.match(r"^\s*(pass|fail|error|skip|warn)\s*$", line)
            if m2:
                res = {
                    "fmf_path": current_test,
                    "status": m2.group(1),
                    "fail_reason": "",
                    "output": "",
                }
                results.append(res)
                # If failed, subsequent lines may contain failure details (output: ...); hang to capture
                if m2.group(1) in ("fail", "error"):
                    pending_result = res
                else:
                    pending_result = None
                    current_test = None
                continue
            # Capture failure details from the pending result
            if pending_result is not None:
                stripped = line.strip()
                if stripped and (stripped.startswith("output:")
                                 or stripped.startswith("/tmp/")
                                 or stripped.startswith("::")):
                    current_fail_reason.append(stripped)
                    pending_result["fail_reason"] = " | ".join(current_fail_reason)[:1000]
                elif not stripped:
                    continue
                else:
                    # Non-detail line (next stage header etc.) — stop capturing
                    pending_result = None
                    current_test = None
                    continue
            elif line.strip():
                stripped = line.strip()
                if not stripped.startswith(_NOISE):
                    pass  # Ignore other lines

    # Filter: keep only cases belonging to this suite
    valid = [r for r in results if r["fmf_path"] in set(case_fmf_paths) or
             r["fmf_path"].startswith("/tests/functional/pkgs/")]
    # Add cases missing from output (mark as error)
    covered = {r["fmf_path"] for r in valid}
    for p in case_fmf_paths:
        if p not in covered:
            valid.append({
                "fmf_path": p,
                "status": "error",
                "fail_reason": "no tmt output for this case",
                "output": "",
            })
    return valid


def _run_direct_suite(ssh: SSHClient, ssh_pw: str, suite_fmf_path: str,
                      case_fmf_paths: List[str], timeout: int) -> List[Dict]:
    """When tmt is unavailable, execute each case script directly via beakerlib.

    Case-by-case execution: a single case timeout/exception only marks that
    case as error, without aborting the entire suite, so completed case
    results are never lost.
    """
    normalized: List[Dict] = []
    for path in case_fmf_paths:
        try:
            results = run_tests_direct(
                ssh, ssh_pw,
                repo_dir=_REMOTE_DIR,
                test_paths=[path],
                suite_paths=[],
                timeout=timeout,
            )
            for r in results:
                normalized.append({
                    "fmf_path": r["test_path"],
                    "status": r["status"],
                    "fail_reason": "" if r["status"] == "pass"
                    else (r.get("final_result") or "failed"),
                    "output": r.get("output", ""),
                })
        except Exception as exc:  # noqa: BLE001
            logger.error("[exec] %s: case %s failed with exception, "
                         "marking as error: %s", suite_fmf_path, path, exc)
            normalized.append({
                "fmf_path": path,
                "status": "error",
                "fail_reason": f"execution raised: {exc}",
                "output": "",
            })
    return normalized
