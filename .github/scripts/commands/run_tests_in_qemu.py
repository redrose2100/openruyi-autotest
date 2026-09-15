# -*- coding: utf-8 -*-
"""
run-tests-in-qemu 命令

流水线步骤 4：在 CloudPods host 上启动的 openRuyi QEMU 虚拟机中执行测试。

流程：
  1. 将 runner 上 checkout 的 PR 代码打包并上传到 QEMU 虚拟机
  2. 在 QEMU 中安装 tmt / beakerlib（参考 docs/user_guide_zh.md）
  3. 配置 topology.env（指向本机）
  4. 执行 tmt run（只运行 PR 改动的测试路径）；tmt 不可用时回退
     直接以 beakerlib 方式执行测试脚本
  5. 解析输出（pass/fail/error），汇总到 test_results.json

输出（JSON）：
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
    """兼容辅助：exec 返回 ExecResult，这里解包为 (code, stdout, stderr) 三元组"""
    r = ssh.exec(cmd, **kw)
    return r.code, r.stdout, r.stderr



logger = logging.getLogger("ci_cli.commands.run_tests_in_qemu")


# ============================================================
# 打包仓库（排除 .git 等）
# ============================================================
def package_repo(repo_root: Path) -> str:
    """把仓库打包为 tar.gz（排除 .git 与无关大目录），返回临时文件路径"""
    fd, tmp = tempfile.mkstemp(suffix=".tar.gz")
    os.close(fd)

    excludes = [".git", "docs", ".github", "unittests"]
    with tarfile.open(tmp, "w:gz") as tar:
        for child in sorted(repo_root.iterdir()):
            if child.name in excludes:
                continue
            tar.add(child, arcname=f"openruyi-autotest/{child.name}")
    return tmp


# ============================================================
# QEMU 内准备与执行
# ============================================================
def _setup_ruamel_pure_python(ssh: SSHClient, sudo_pw: str) -> bool:
    """在 QEMU 内强制 ruamel.yaml 使用纯 Python 解析（禁用 C 扩展）。

    背景：openruyi riscv64 仓库提供预编译 python-ruamel-yaml-clib（C 扩展），
    fmf 1.7.0 的 grow() 用 YAML(typ="safe") 解析 main.fmf，safe 模式在 clib
    存在时走 CParser（C 扩展）而非纯 Python Parser，而该 C 扩展在 riscv64 上
    解析 YAML 会死循环/极慢（与上游 s390x 已知问题 fmf/issues/164 同族），
    导致 fmf.Tree('.') 扫描卡死、tmt discover 无限挂起。

    方案：写一个 sitecustomize.py 到 site-packages（Python 启动时自动加载），
    把 ruamel.yaml 的 CParser/CEmitter 置为 None，使 YAML(typ="safe") 回退到
    纯 Python Parser（本地 x86_64 纯 Python 实测扫描 4150 节点仅 ~10s）。
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
    # 找到 site-packages 路径。所有 sudo 命令都通过 `-S` 从管道读密码
    # （不能用 heredoc 做 python3 stdin，因为 heredoc 会覆盖管道导致 sudo
    # 读不到密码；也不能依赖 sudo 时间戳缓存，QEMU 里可能被禁用）。
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S python3 -c \"import site; "
        "print(site.getsitepackages()[0])\" 2>&1",
        timeout=60)
    sp = out.strip().splitlines()[-1].strip() if out.strip() else ""
    if code != 0 or not sp or not sp.startswith("/"):
        logger.warning("[QEMU] cannot locate site-packages, skip ruamel fix: %r", out[-300:])
        return False
    # 写入 sitecustomize.py。sudo -S 从外部管道读密码，bash -c 内部
    # echo->base64->重定向到文件，两条管道互不干扰。
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
    # 验证纯 Python 生效：CParser 应为 None，且能正常 load YAML
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
    """在 QEMU 中安装测试执行环境。

    返回安装方式：
      - "tmt"   ：tmt 可用（dnf 或 pip 安装成功且 fmf 扫描正常）
      - "direct"：tmt 不可用，但 beakerlib 可用（改用直接执行测试脚本）
      - ""      ：两者都失败
    """
    # 确保 sudo 免密可用
    ssh.exec(f"echo '{sudo_pw}' | sudo -S true")

    # 1. 基础工具：tar / beakerlib（QEMU 最小系统可能缺失）。注意 openruyi 的
    #    https repo 有 SSL 证书问题，dnf 必须 --nogpgcheck --setopt=sslverify=0。
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S dnf install -y --nogpgcheck "
        "--setopt=sslverify=0 tar gzip python3-pip beakerlib python-six 2>&1 | tail -20",
        timeout=1800,
    )
    if code != 0 and "Nothing to do" not in out:
        logger.warning("[QEMU] dnf install tar/pip/beakerlib failed: code=%s\n%s\n%s",
                       code, out, err)
        return ""

    # 2. 优先用 dnf 装 tmt（openruyi 仓库有 python-tmt + ruamel-yaml-clib rpm，
    #    避免 pip 在 riscv64 上编译 C 扩展）
    code, out, err = _exec3(ssh,
        f"echo '{sudo_pw}' | sudo -S dnf install -y --nogpgcheck "
        "--setopt=sslverify=0 tmt 2>&1 | tail -15",
        timeout=1800,
    )
    if code == 0:
        code2, out2, err2 = _exec3(ssh, "tmt --version", timeout=60)
        if code2 == 0:
            # tmt 可用。但在 riscv64 上 openruyi 的 python-ruamel-yaml-clib
            # C 扩展会让 fmf 的 YAML(typ="safe") 走 CParser 并卡死（与 s390x
            # 已知问题同族）。先强制 ruamel 纯 Python 解析，根治扫描卡死。
            _setup_ruamel_pure_python(ssh, sudo_pw)
            # 自检 fmf 扫描：fmf.Tree 没有 .tests 属性（那是 tmt 的 API），
            # 用 climb() 统计节点数。扫描能完成即判定 tmt 可用。
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

    # 3. dnf 失败回退 pip：先装编译工具链，再 pip 装 tmt
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
            # 同 dnf 路径：先强制 ruamel 纯 Python，再自检 fmf 扫描
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

    # 4. tmt 彻底不可用：退化为直接执行 beakerlib 测试脚本
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
    """tmt 不可用时，直接在 QEMU 里以 beakerlib 方式执行测试脚本。

    对于每个测试路径（/tests/functional/pkgs/acl/test_acl_getfacl_basic 形式），
    转换为仓库内相对路径，在 QEMU 内读取 main.fmf 的 test: 字段（或回退
    test.sh/runtest.sh），然后用 bash 执行该脚本；用 beakerlib 的日志输出
    判断 PASS/FAIL。

    注意：脚本运行在 runner 上，repo 文件在 QEMU VM 内，因此所有文件系统
    操作都必须通过 ssh 在 QEMU 内完成，不能用本地的 os.path.isfile。
    """
    results: List[Dict] = []
    targets = list(test_paths) + list(suite_paths)
    for target in targets:
        # /tests/functional/... -> tests/functional/...
        rel = target.lstrip("/")
        test_dir = os.path.join(repo_dir, rel).replace(os.sep, "/")
        # 在 QEMU 内读取 main.fmf 的 test: 字段（或回退 test.sh/runtest.sh/test）
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
        # source topology.env 提供 TEST_SERVER_* 环境变量，同时 export 兜底密码
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
        # beakerlib 输出（1.30+ 带时间戳/方括号）：
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
    return results


def remote_setup_topology(ssh: SSHClient, sudo_pw: str, host_ip: str) -> bool:
    """配置 topology.env 指向本机（单机模式）"""
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
    """执行 tmt，返回每个测试用例的结果"""
    results: List[Dict] = []

    # 构造 tmt 命令（先 suite 后 case，按路径过滤）
    targets = list(suite_paths) + list(test_paths)
    if not targets:
        return results

    # tmt 允许 --name 传多次，一次执行所有目标
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

    # 解析 tmt 树状输出中的用例状态
    # 格式示例：
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
                # 非标准行，忽略
                pass

    if not results:
        # 解析失败时退化：检查 tmt 输出中 "pass" / "fail" 计数
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

    # 汇总
    summary = {"pass": 0, "fail": 0, "error": 0, "skip": 0}
    for r in results:
        s = r["status"]
        summary[s] = summary.get(s, 0) + 1
    return results


class RunTestsInQemuCommand(BaseCommand):
    """在 QEMU 虚拟机中运行 PR 改动的测试"""

    name = "run-tests-in-qemu"
    description = "在 CloudPods 的 QEMU 虚拟机中运行 PR 改动测试并汇总结果"

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

        # 1. 打包仓库
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
                    # 2. 先确保 tar 存在（QEMU 最小系统可能没有，解压依赖它）
                    ssh.exec(f"echo '{ssh_pw}' | sudo -S true")
                    code, out, err = _exec3(ssh, "command -v tar", timeout=30)
                    if code != 0:
                        # 注意：安装命令不能用 "| tail" 收尾（管道会吞掉 dnf
                        # 的退出码导致误判成功），且 openruyi 的 https repo 有
                        # SSL 证书问题，必须 --setopt=sslverify=0；安装完成后
                        # 必须重新验证 command -v tar。
                        code, out, err = _exec3(ssh,
                            f"echo '{ssh_pw}' | sudo -S dnf install -y "
                            "--nogpgcheck --setopt=sslverify=0 tar gzip 2>&1 | tail -5",
                            timeout=600,
                        )
                        code, out, err = _exec3(ssh, "command -v tar", timeout=30)
                        if code != 0:
                            raise RuntimeError(f"install tar failed: {out} {err}")

                    # 3. 上传并解压仓库
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

                    # 4. 准备环境（tmt/beakerlib）
                    exec_mode = remote_prepare_env(ssh, ssh_pw)
                    if not exec_mode:
                        raise RuntimeError("prepare env failed")

                    # 5. 配置 topology.env
                    remote_setup_topology(ssh, ssh_pw, host_ip)

                    # 6. 运行测试（tmt 或直接 beakerlib）
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

        # 清理临时 tarball
        try:
            os.remove(tarball)
        except OSError:
            pass

        # 汇总
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
