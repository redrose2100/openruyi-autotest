# -*- coding: utf-8 -*-
"""
run-tests-in-qemu command

Pipeline step 4: run tests in the openRuyi QEMU VM launched on CloudPods host.

Workflow:
  1. Package PR code checked out on runner and upload to QEMU VM
  2. Install tmt / beakerlib in QEMU (see docs/user_guide.md)
  3. Configure topology.env (point to localhost)
  4. Run tmt run (only changed test paths from PR); fall back to direct
     beakerlib execution when tmt is unavailable
  5. Parse output (pass/fail/error), summarize to test_results.json

Output (JSON):
  {
    "ok": true/false,
    "results": [{"host_ip","qemu_port","test_path","status","output"}],
    "summary": {"pass":1,"fail":0,"error":0,"skip":0,"total":1}
  }
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional

from core.base import BaseCommand
from core.ssh import SSHClient


def _exec3(ssh: SSHClient, cmd: str, **kw):
    """Compatibility helper: unpack ExecResult into (code, stdout, stderr) tuple."""
    r = ssh.exec(cmd, **kw)
    return r.code, r.stdout, r.stderr



logger = logging.getLogger("ci_cli.commands.run_tests_in_qemu")


# ============================================================
# Package repo (exclude .git etc.)
# ============================================================
def package_repo(repo_root: Path, excludes=None) -> str:
    """Package repo as tar.gz (excluding .git and unrelated large dirs),
    return temp file path.

    excludes can be a list of additional dir names to exclude (e.g. for
    functional full test, exclude performance/ etc. to reduce tarball size).
    """
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


# ============================================================
# QEMU prep and execution
# ============================================================
def _setup_ruamel_pure_python(ssh: SSHClient, sudo_pw: str) -> bool:
    """Force ruamel.yaml to use pure-Python parser inside QEMU (disable C ext).

    Background: openruyi riscv64 repo provides prebuilt python-ruamel-yaml-clib
    (C extension). fmf 1.7.0's grow() uses YAML(typ="safe") to parse main.fmf;
    with clib present, safe mode uses CParser (C ext) instead of pure Python
    Parser. The C extension hangs / is extremely slow on riscv64 (same family
    as the known s390x issue fmf/issues/164), causing fmf.Tree('.') scan to
    freeze and tmt discover to hang indefinitely.

    Solution: write a sitecustomize.py to site-packages (auto-loaded on Python
    startup) that sets ruamel.yaml's CParser/CEmitter to None, making
    YAML(typ="safe") fall back to pure Python Parser (local x86_64 pure Python
    scan of 4150 nodes takes only ~10s).
    """
    sitecustomize = r'''# -*- coding: utf-8 -*-
"""Force ruamel.yaml to use pure-Python parser (riscv64 clib hang workaround).

openruyi riscv64 python-ruamel-yaml-clib C extension hangs/slows down YAML
parsing on riscv64 (same family as the s390x issue fmf/issues/164). Setting
CParser/CEmitter to None makes YAML(typ="safe") fall back to the pure-Python
parser which is known to work (local x86_64 scan of 4150 nodes ~10s).
"""
import sys

# Block imports of the C extension modules so CParser/CEmitter stay None
try:
    import ruamel.yaml.main
    import ruamel.yaml.cyaml
    for module in (ruamel.yaml.main, ruamel.yaml.cyaml):
        module.CParser = None
        module.CEmitter = None
    # In case YAML was already instantiated, patch module-level names too
    sys.modules.setdefault('ruamel.yaml.main', ruamel.yaml.main)
    sys.modules.setdefault('ruamel.yaml.cyaml', ruamel.yaml.cyaml)
except Exception:
    pass
'''
    # Locate site-packages path. All sudo commands read password from pipe via `-S`
    # (cannot use heredoc for python3 stdin because heredoc would overwrite the pipe
    # causing sudo to miss the password; also can't rely on sudo timestamp cache
    # which may be disabled in QEMU).
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S python3 -c \"import site; "
        "print(site.getsitepackages()[0])\" 2>&1",
        timeout=60)
    sp = out.strip().splitlines()[-1].strip() if out.strip() else ""
    if code != 0 or not sp or not sp.startswith("/"):
        logger.warning("[QEMU] cannot locate site-packages, skip ruamel fix: %r", out[-300:])
        return False
    # Write sitecustomize.py. sudo -S reads password from external pipe,
    # bash -c internally echo->base64->redirect to file, two pipes don't interfere.
    import base64
    b64 = base64.b64encode(sitecustomize.encode("utf-8")).decode("ascii")
    write_cmd = (
        f"echo '{sudo_pw}' | sudo -S bash -c "
        f"'echo {b64} | base64 -d > {sp}/sitecustomize.py' 2>&1"
    )
    code2, out2, err2 = _exec3(ssh, write_cmd, timeout=60)
    if code2 != 0:
        logger.warning("[QEMU] failed to write sitecustomize.py: %s %s", out2[-300:], err2[-300:])
        return False
    # Verify pure-Python mode works: CParser should be None, and YAML loads normally
    verify = (
        f"echo '{sudo_pw}' | sudo -S python3 -c \"import ruamel.yaml; "
        "from ruamel.yaml.main import CParser; "
        "print('RUAMEL_CPARSER_NONE' if CParser is None else 'RUAMEL_CPARSER_SET'); "
        "from ruamel.yaml import YAML; data = YAML(typ='safe').load('a: 1'); "
        "print('RUAMEL_LOAD_OK', data.get('a'))\" 2>&1"
    )
    code3, out3, err3 = _exec3(ssh, verify, timeout=60)
    ok = code3 == 0 and "RUAMEL_CPARSER_NONE" in out3 and "RUAMEL_LOAD_OK" in out3
    logger.info("[QEMU] ruamel pure-python fix: %s (out=%s)",
                "ok" if ok else "failed", out3.strip()[-300:])
    return ok


def remote_prepare_env(ssh: SSHClient, sudo_pw: str) -> str:
    """Install test execution environment inside QEMU.

    Returns the installation method:
      - "tmt"   : tmt available (dnf or pip install succeeded and fmf scan works)
      - "direct": tmt unavailable, but beakerlib available (fall back to direct script exec)
      - ""      : both failed
    """
    # Ensure sudo works without password prompt
    ssh.exec(f"echo '{sudo_pw}' | sudo -S true")

    # 1. Basic tools: tar / beakerlib (QEMU minimal system may lack these). Note that
    #    openruyi's https repo has SSL certificate issues, so dnf needs
    #    --nogpgcheck --setopt=sslverify=0.
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S dnf install -y --nogpgcheck "
        "--setopt=sslverify=0 tar gzip python3-pip beakerlib python-six 2>&1 | tail -20",
        timeout=1800,
    )
    if code != 0 and "Nothing to do" not in out:
        logger.warning("[QEMU] dnf install tar/pip/beakerlib failed: code=%s\n%s\n%s",
                       code, out, err)
        return ""

    # 2. Prefer dnf for tmt (openruyi repo has python-tmt + ruamel-yaml-clib rpm,
    #    avoiding pip compiling C extensions on riscv64)
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S dnf install -y --nogpgcheck "
        "--setopt=sslverify=0 tmt 2>&1 | tail -15",
        timeout=1800,
    )
    if code == 0:
        code2, out2, err2 = _exec3(ssh, "tmt --version", timeout=60)
        if code2 == 0:
            # tmt is available. But on riscv64, openruyi's python-ruamel-yaml-clib
            # C extension causes fmf's YAML(typ="safe") to go through CParser and
            # hang (same family as the known s390x issue). Force ruamel pure-Python
            # parsing first to prevent scan hangs.
            _setup_ruamel_pure_python(ssh, sudo_pw)
            # Self-check fmf scan: fmf.Tree has no .tests attribute (that's tmt API),
            # use climb() to count nodes. If scan completes, tmt is considered usable.
            logger.info("[QEMU] tmt ready (dnf): %s, checking fmf scan...", out2.strip()[:200])
            probe = (
                "cd ~/openruyi-autotest && "
                "timeout 60 python3 -c \"import fmf,time;t0=time.time();"
                "t=fmf.Tree('.');n=sum(1 for _ in t.climb());"
                "print('FMF_SCAN_OK',round(time.time()-t0,1),'nodes',n)\" 2>&1 | tail -3"
            )
            pcode, pout, perr = _exec3(ssh, probe, timeout=120)
            if pcode == 0 and "FMF_SCAN_OK" in pout:
                logger.info("[QEMU] fmf scan OK: %s", pout.strip()[-120:])
                return "tmt"
            logger.warning("[QEMU] fmf scan failed/timeout, tmt unusable: code=%s "
                           "out=%r err=%r", pcode, pout[-300:], perr[-200:])
            logger.warning("[QEMU] falling back to direct beakerlib execution")

    logger.warning("[QEMU] dnf tmt failed: code=%s\n%s\n%s", code, out[-1500:], err[-500:])

    # 3. dnf failed, fallback to pip: install build toolchain first, then pip install tmt
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S dnf install -y --nogpgcheck "
        "--setopt=sslverify=0 gcc gcc-c++ python3-devel rust cargo 2>&1 | tail -10",
        timeout=1800,
    )
    if code != 0 and "Nothing to do" not in out:
        logger.warning("[QEMU] dnf install toolchain failed (non-fatal): code=%s", code)

    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S pip3 install --break-system-packages tmt 2>&1 | tail -30",
        timeout=1800,
    )
    if code == 0:
        code2, out2, err2 = _exec3(ssh, "tmt --version", timeout=60)
        if code2 == 0:
            # Same as dnf path: force ruamel pure Python first, then self-check fmf scan
            _setup_ruamel_pure_python(ssh, sudo_pw)
            logger.info("[QEMU] tmt ready (pip): %s, checking fmf scan...", out2.strip()[:200])
            probe = (
                "cd ~/openruyi-autotest && "
                "timeout 60 python3 -c \"import fmf,time;t0=time.time();"
                "t=fmf.Tree('.');n=sum(1 for _ in t.climb());"
                "print('FMF_SCAN_OK',round(time.time()-t0,1),'nodes',n)\" 2>&1 | tail -3"
            )
            pcode, pout, perr = _exec3(ssh, probe, timeout=120)
            if pcode == 0 and "FMF_SCAN_OK" in pout:
                logger.info("[QEMU] fmf scan OK: %s", pout.strip()[-120:])
                return "tmt"
            logger.warning("[QEMU] fmf scan failed/timeout, tmt unusable: code=%s "
                           "out=%r err=%r", pcode, pout[-300:], perr[-200:])
            logger.warning("[QEMU] falling back to direct beakerlib execution")

    logger.warning("[QEMU] pip tmt install failed: code=%s\n%s\n%s", code, out[-2000:], err[-500:])

    # 4. tmt completely unavailable: fall back to direct beakerlib test script execution
    code, out, err = _exec3(ssh,
        "test -f /usr/share/beakerlib/beakerlib.sh && echo ok", timeout=60)
    if code == 0:
        logger.info("[QEMU] tmt unavailable, will run tests directly with beakerlib")
        return "direct"
    logger.warning("[QEMU] beakerlib not found either, tests cannot run")
    return ""


def run_tests_direct(ssh: SSHClient, sudo_pw: str, repo_dir: str,
                     test_paths: List[str], suite_paths: List[str],
                     timeout: int = 5400) -> List[Dict]:
    """When tmt is unavailable, execute test scripts directly in QEMU via beakerlib.

    For each test path (e.g. /tests/functional/pkgs/acl/test_acl_getfacl_basic format),
    convert to a repo-relative path, read the main.fmf test: field inside QEMU (or fall
    back to test.sh/runtest.sh), then run the script with bash; use beakerlib log output
    to determine PASS/FAIL.

    Note: the script runs on the runner but repo files are inside the QEMU VM, so all
    filesystem operations must be done via ssh inside QEMU, not using local os.path.isfile.
    """
    results: List[Dict] = []
    targets = list(test_paths) + list(suite_paths)
    for target in targets:
        # /tests/functional/... -> tests/functional/...
        rel = target.lstrip("/")
        test_dir = os.path.join(repo_dir, rel).replace(os.sep, "/")
        # Read main.fmf test: field inside QEMU (or fall back to test.sh/runtest.sh/test)
        script_rel = None
        fmf_file = os.path.join(test_dir, "main.fmf")
        code, out, err = _exec3(ssh,
            f"cat {fmf_file} 2>/dev/null | grep -E '^[[:space:]]*test:' | head -1",
            timeout=30,
        )
        if code == 0 and out.strip():
            script_rel = out.strip().split(":", 1)[1].strip().strip('"').strip("'")
        if not script_rel:
            for cand in ("test.sh", "runtest.sh", "test"):
                c2, o2, e2 = _exec3(ssh, f"test -f {test_dir}/{cand} && echo ok", timeout=30)
                if c2 == 0 and "ok" in o2:
                    script_rel = cand
                    break
        if not script_rel:
            logger.warning("[QEMU] direct: no test script found for %s, skip", target)
            continue
        remote_script = os.path.join(test_dir, script_rel).replace(os.sep, "/")
        # source topology.env to provide TEST_SERVER_* env vars, also export fallback password
        cmd = (
            f"cd {os.path.dirname(remote_script)} && "
            f"set -a && . {repo_dir}/topology.env 2>/dev/null; set +a; "
            f"export TEST_SERVER_1_PASSWORD='{sudo_pw}'; "
            f"echo '{sudo_pw}' | sudo -S true && "
            f"bash {remote_script} 2>&1"
        )
        logger.info("[QEMU] direct running: %s...", cmd[:200])
        code, out, err = _exec3(ssh, cmd, timeout=timeout)
        output = out + ("\n[stderr]\n" + err if err else "")
        # beakerlib output (1.30+ with timestamp/brackets):
        #   :: [ 15:43:03 ] :: [   PASS   ] :: message
        #   ::   RESULT: PASS
        #   ::   OVERALL RESULT: PASS
        overall_m = re.search(r"OVERALL RESULT:\s*(PASS|FAIL|WARN|ERROR)", output)
        result_m = re.search(r"::\s+RESULT:\s*(PASS|FAIL|WARN|ERROR)", output)
        final = (overall_m or result_m).group(1) if (overall_m or result_m) else None
        pass_n = len(re.findall(r"::\s+\[[^\]]*\]\s*::\s*\[\s*PASS\s*\]", output))
        fail_n = len(re.findall(r"::\s+\[[^\]]*\]\s*::\s*\[\s*FAIL\s*\]", output))
        if final == "PASS":
            status = "pass"
        elif final in ("FAIL", "ERROR"):
            status = "fail"
        elif fail_n or code != 0:
            status = "fail"
        elif pass_n:
            status = "pass"
        else:
            status = "error"
        results.append({
            "test_path": target,
            "status": status,
            "output": output[-4000:],
            "runner": "direct",
            "final_result": final or "none",
            "pass_lines": pass_n,
            "fail_lines": fail_n,
        })
        logger.info("[QEMU] direct result for %s: %s (final=%s pass=%s fail=%s exit=%s)",
                    target, status, final, pass_n, fail_n, code)
        if status == "fail":
            fail_lines = [l for l in output.splitlines() if ":: [   FAIL   ] ::" in l or ":: [  FAIL  ] ::" in l]
            if fail_lines:
                logger.info("[QEMU] FAIL details for %s:\n%s", target, "\n".join(fail_lines[-20:]))
            # Also log the last 100 lines of output for FAIL cases
            tail_lines = output.splitlines()[-100:]
            logger.info("[QEMU] output tail for %s:\n%s", target, "\n".join(tail_lines))
    return results


def remote_setup_topology(ssh: SSHClient, sudo_pw: str, host_ip: str) -> bool:
    """Configure topology.env to point to localhost (single-machine mode)."""
    content = (
        "TEST_SERVER_COUNT=1\n"
        f"TEST_SERVER_1_HOST=127.0.0.1\n"
        "TEST_SERVER_1_PORT=22\n"
        "TEST_SERVER_1_USER=openruyi\n"
        f"TEST_SERVER_1_PASSWORD={sudo_pw}\n"
    )
    code, out, err = _exec3(ssh,
        f"cat > ~/openruyi-autotest/topology.env << 'EOF'\n{content}\nEOF",
        timeout=30,
    )
    return code == 0


def run_tmt_tests(ssh: SSHClient, sudo_pw: str, test_paths: List[str],
                  suite_paths: List[str], timeout: int = 5400) -> List[Dict]:
    """Execute tmt, return results for each test case."""
    results: List[Dict] = []

    # Build tmt command (suites first, then cases, filtered by path)
    targets = list(suite_paths) + list(test_paths)
    if not targets:
        return results

    # tmt allows --name to be passed multiple times, running all targets in one go
    name_args = " ".join(f"--name {p}" for p in targets)

    cmd = (
        f"cd ~/openruyi-autotest && "
        f"echo '{sudo_pw}' | sudo -S true && "
        f"timeout 1500 tmt run --all plan --name /plans/functional {name_args} "
        f"provision --feeling-safe 2>&1"
    )
    logger.info("[QEMU] Running: %s...", cmd[:300])
    code, out, err = _exec3(ssh, cmd, timeout=timeout)

    output = out + ("\n[stderr]\n" + err if err else "")
    logger.info("[QEMU] tmt exit=%s, output length=%s", code, len(output))

    # Parse case statuses from tmt tree-style output
    # Format example:
    #   /tests/functional/pkgs/acl/test_acl_getfacl_basic
    #       pass
    lines = output.splitlines()
    current_test = None
    for i, line in enumerate(lines):
        m = re.match(r"^\s*(/tests/\S+)\s*$", line)
        if m:
            current_test = m.group(1)
            continue
        if current_test:
            m2 = re.match(r"^\s*(pass|fail|error|skip|warn)\s*$", line)
            if m2:
                results.append({
                    "test_path": current_test,
                    "status": m2.group(1),
                })
                current_test = None
            elif line.strip() and not line.strip().startswith((
                "discover", "provision", "prepare", "execute", "report", "plan",
                "summary", "1 test", "total", "output", "Result"
            )):
                # Non-standard line, ignore
                pass

    if not results:
        # Degrade when parse fails: check "pass" / "fail" count in tmt output
        pass_count = len(re.findall(r"^\s+pass\s*$", output, re.MULTILINE))
        fail_count = len(re.findall(r"^\s+fail\s*$", output, re.MULTILINE))
        error_count = len(re.findall(r"^\s+error\s*$", output, re.MULTILINE))
        for p in targets:
            results.append({
                "test_path": p,
                "status": "fail" if (fail_count or error_count or code != 0) else "pass",
                "fallback": True,
            })
        for r in results:
            r["output"] = output[-4000:]
    else:
        for r in results:
            r["output"] = output[-4000:]

    # Summarize
    summary = {"pass": 0, "fail": 0, "error": 0, "skip": 0}
    for r in results:
        s = r["status"]
        summary[s] = summary.get(s, 0) + 1
    return results


class RunTestsInQemuCommand(BaseCommand):
    """Run PR-changed tests in QEMU VMs"""

    name = "run-tests-in-qemu"
    description = "Run PR-changed tests in CloudPods QEMU VMs and aggregate results"

    def setup_parser(self, parser):
        parser.add_argument("--vm-info", required=True, help="Path to vm_info.json")
        parser.add_argument("--repo", required=True,
                            help="Repository root (checked out PR)")
        parser.add_argument("--requirements", required=True,
                            help="Path to vm_requirements.json")
        parser.add_argument("--output", required=True,
                            help="Output test_results.json path")

    def run(self, args) -> int:
        with open(args.vm_info, encoding="utf-8") as f:
            vm_info = json.load(f)
        with open(args.requirements, encoding="utf-8") as f:
            req = json.load(f)

        hosts = vm_info.get("hosts", [])
        test_paths = req.get("test_paths", [])
        suite_paths = req.get("suite_paths", [])
        if not hosts:
            self.log_error("No hosts in vm_info")
            return 1

        repo_root = Path(args.repo).resolve()

        # 1. Package repository
        self.log_info("Packaging repository...")
        tarball = package_repo(repo_root)
        self.log_info(f"Packed: {tarball}")

        all_results: List[Dict] = []
        overall_ok = True

        for host in hosts:
            host_ip = host["host_ip"]
            ssh_user = host.get("ssh_user", "openruyi")
            ssh_pw = host.get("ssh_password", "openruyi")
            host_pw = host.get("host_ssh_password", "ISRCpassword@123")

            for qemu_port in host.get("qemu_ports", []):
                self.log_info(f"{'='*60}\nQEMU VM: {host_ip}:{qemu_port}\n{'='*60}")
                try:
                    ssh = SSHClient(host_ip, qemu_port, ssh_user, ssh_pw)
                except Exception as e:  # noqa: BLE001
                    self.log_error(f"SSH connect failed {host_ip}:{qemu_port}: {e}")
                    for p in test_paths + suite_paths:
                        all_results.append({
                            "host_ip": host_ip, "qemu_port": qemu_port,
                            "test_path": p, "status": "error",
                            "output": f"SSH connect failed: {e}",
                        })
                    overall_ok = False
                    continue

                try:
                    # 2. Ensure tar exists first (minimal QEMU system may lack it; extraction depends on it)
                    ssh.exec(f"echo '{ssh_pw}' | sudo -S true")
                    code, out, err = _exec3(ssh, "command -v tar", timeout=30)
                    if code != 0:
                        # Note: the install command must not end with "| tail" (the pipe swallows
                        # dnf exit codes causing false success), and openruyi's https repo has
                        # SSL certificate issues, so --setopt=sslverify=0 is required; after
                        # installation, re-verify with command -v tar.
                        code, out, err = _exec3(ssh,
                            f"echo '{ssh_pw}' | sudo -S dnf install -y "
                            "--nogpgcheck --setopt=sslverify=0 tar gzip 2>&1 | tail -5",
                            timeout=600,
                        )
                        code, out, err = _exec3(ssh, "command -v tar", timeout=30)
                        if code != 0:
                            raise RuntimeError(f"install tar failed: {out} {err}")

                    # 3. Upload and extract repository
                    remote_dir = "/home/openruyi/openruyi-autotest"
                    ssh.exec(f"rm -rf {remote_dir}")
                    ssh.exec("mkdir -p /home/openruyi")
                    if not ssh.put_file(tarball, "/home/openruyi/repo.tar.gz"):
                        raise RuntimeError("upload repo failed")
                    code, out, err = _exec3(ssh,
                        "cd /home/openruyi && tar xzf repo.tar.gz && rm -f repo.tar.gz",
                        timeout=300)
                    if code != 0:
                        raise RuntimeError(f"extract failed: {out} {err}")

                    # 4. Prepare environment (tmt/beakerlib)
                    exec_mode = remote_prepare_env(ssh, ssh_pw)
                    if not exec_mode:
                        raise RuntimeError("prepare env failed")

                    # 5. Configure topology.env
                    remote_setup_topology(ssh, ssh_pw, host_ip)

                    # 6. Run tests (tmt or direct beakerlib)
                    if exec_mode == "tmt":
                        vm_results = run_tmt_tests(ssh, ssh_pw, test_paths, suite_paths)
                    else:
                        vm_results = run_tests_direct(
                            ssh, ssh_pw,
                            repo_dir="/home/openruyi/openruyi-autotest",
                            test_paths=test_paths, suite_paths=suite_paths,
                        )
                    for r in vm_results:
                        r["host_ip"] = host_ip
                        r["qemu_port"] = qemu_port
                    all_results.extend(vm_results)
                    if not vm_results:
                        overall_ok = False
                except Exception as e:  # noqa: BLE001
                    self.log_error(f"Error on {host_ip}:{qemu_port}: {e}")
                    for p in test_paths + suite_paths:
                        all_results.append({
                            "host_ip": host_ip, "qemu_port": qemu_port,
                            "test_path": p, "status": "error",
                            "output": str(e),
                        })
                    overall_ok = False
                finally:
                    ssh.close()

        # Clean up temp tarball
        try:
            os.remove(tarball)
        except OSError:
            pass

        # Summary
        summary = {"pass": 0, "fail": 0, "error": 0, "skip": 0, "total": len(all_results)}
        for r in all_results:
            summary[r["status"]] = summary.get(r["status"], 0) + 1

        result = {
            "ok": overall_ok and summary.get("fail", 0) == 0 and summary.get("error", 0) == 0,
            "results": all_results,
            "summary": summary,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        self.log_info(f"\nSummary: {json.dumps(summary)}")
        return 0 if result["ok"] else 1
