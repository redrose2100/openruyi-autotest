#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_tests_in_qemu.py

流水线步骤 4：在 CloudPods host 上启动的 openRuyi QEMU 虚拟机中，
模拟手工测试方式执行 PR 中修改的测试脚本：

  1. 将 runner 上 checkout 的 PR 代码打包并上传到 QEMU 虚拟机
  2. 在 QEMU 中安装 tmt / beakerlib（参考 docs/user_guide_zh.md）
  3. 配置 topology.env（指向本机）
  4. 执行 tmt run（只运行 PR 改动的测试路径）
  5. 解析 tmt 输出（pass/fail/error），汇总到 test_results.json

输出（JSON）：
  {
    "ok": true/false,
    "results": [
      {
        "host_ip": "...", "qemu_port": 12055,
        "test_path": "/tests/functional/pkgs/acl/test_acl_getfacl_basic",
        "status": "pass" | "fail" | "error" | "skip",
        "output": "...",
        "duration": 123
      }
    ],
    "summary": {"pass": 1, "fail": 0, "error": 0}
  }
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import paramiko

# ============================================================
# SSH 工具（轻量封装，与 create_server.py 风格一致）
# ============================================================

class SSHClient:
    def __init__(self, ip: str, port: int, username: str, password: str,
                 connect_timeout: int = 20):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            ip, port=port, username=username, password=password,
            look_for_keys=False, allow_agent=False,
            timeout=connect_timeout,
            banner_timeout=connect_timeout,
            auth_timeout=connect_timeout,
        )

    def exec(self, cmd: str, timeout: int = 600) -> Tuple[int, str, str]:
        """执行命令，返回 (exit_code, stdout, stderr)"""
        transport = self.ssh.get_transport()
        channel = transport.open_session()
        channel.settimeout(timeout)
        try:
            channel.exec_command(cmd)
        except Exception as e:
            return (255, "", str(e))

        stdout_buf, stderr_buf = [], []
        import select
        start = time.time()
        while True:
            if time.time() - start > timeout:
                channel.close()
                return (124, "".join(stdout_buf), "".join(stderr_buf) + "\n[timeout]")
            r, _, _ = select.select([channel], [], [], 1.0)
            if channel in r:
                data = channel.recv(65536)
                if data:
                    stdout_buf.append(data.decode("utf-8", "ignore"))
                err = channel.recv_stderr(65536)
                if err:
                    stderr_buf.append(err.decode("utf-8", "ignore"))
            if channel.exit_status_ready():
                # 命令已退出，排空剩余数据（recv 返回空即 EOF，必须 break 否则忙循环）
                while True:
                    r2, _, _ = select.select([channel], [], [], 0.3)
                    if channel not in r2:
                        break
                    data = channel.recv(65536)
                    if data:
                        stdout_buf.append(data.decode("utf-8", "ignore"))
                    else:
                        break
                    err = channel.recv_stderr(65536)
                    if err:
                        stderr_buf.append(err.decode("utf-8", "ignore"))
                break
        code = channel.recv_exit_status()
        return (code, "".join(stdout_buf), "".join(stderr_buf))

    def put_file(self, local: str, remote: str) -> bool:
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(local, remote)
            sftp.close()
            return True
        except Exception as e:
            print(f"[SSH] upload failed {local} -> {remote}: {e}")
            return False

    def close(self):
        try:
            self.ssh.close()
        except Exception:
            pass


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

def remote_prepare_env(ssh: SSHClient, sudo_pw: str) -> str:
    """在 QEMU 中安装测试执行环境。

    返回安装方式：
      - "tmt"   ：tmt 可用（dnf 或 pip 安装成功）
      - "direct"：tmt 不可用，但 beakerlib 可用（改用直接执行测试脚本）
      - ""      ：两者都失败
    """
    # 确保 sudo 免密可用
    ssh.exec(f"echo '{sudo_pw}' | sudo -S true")

    # 1. 基础工具：tar / beakerlib（QEMU 最小系统可能缺失）
    code, out, err = ssh.exec(
        f"echo '{sudo_pw}' | sudo -S dnf install -y tar gzip python3-pip beakerlib python-six 2>&1 | tail -20",
        timeout=1800,
    )
    if code != 0 and "Nothing to do" not in out:
        print(f"[QEMU] dnf install tar/pip/beakerlib failed: code={code}\n{out}\n{err}")
        # beakerlib 装不上，直接执行也做不了，返回空
        return ""

    # 2. 优先用 dnf 装 tmt（openruyi 仓库有 python-tmt + ruamel-yaml-clib rpm，
    #    避免 pip 在 riscv64 上编译 C 扩展）
    code, out, err = ssh.exec(
        f"echo '{sudo_pw}' | sudo -S dnf install -y tmt 2>&1 | tail -15",
        timeout=1800,
    )
    if code == 0:
        code2, out2, err2 = ssh.exec("tmt --version", timeout=60)
        if code2 == 0:
            # tmt 可用，但还要自检 fmf 扫描：openruyi 的 python-fmf 1.7.0 在
            # riscv64 上扫描 fmf 树可能死循环/极慢（tmt discover 依赖 fmf.Tree），
            # 卡死会导致 tmt run 无限挂起。用 timeout 实测扫描仓库能否完成，
            # 失败则判定 tmt 不可用，回退 direct。
            print(f"[QEMU] tmt ready (dnf): {out2.strip()[:200]}, checking fmf scan...")
            probe = (
                "cd ~/openruyi-autotest && "
                "timeout 60 python3 -c \"import fmf,time;t0=time.time();"
                "t=fmf.Tree('.');print('FMF_SCAN_OK',round(time.time()-t0,1),"
                "'tests',len(t.tests))\" 2>&1 | tail -3"
            )
            pcode, pout, perr = ssh.exec(probe, timeout=120)
            if pcode == 0 and "FMF_SCAN_OK" in pout:
                print(f"[QEMU] fmf scan OK: {pout.strip()[-120:]}")
                return "tmt"
            print(f"[QEMU] fmf scan failed/timeout, tmt unusable: code={pcode} "
                  f"out={pout[-300:]!r} err={perr[-200:]!r}")
            print("[QEMU] falling back to direct beakerlib execution")

    print(f"[QEMU] dnf tmt failed: code={code}\n{out[-1500:]}\n{err[-500:]}")

    # 3. dnf 失败回退 pip：先装编译工具链，再 pip 装 tmt（完整输出，不截断）
    code, out, err = ssh.exec(
        f"echo '{sudo_pw}' | sudo -S dnf install -y gcc gcc-c++ python3-devel rust cargo 2>&1 | tail -10",
        timeout=1800,
    )
    if code != 0 and "Nothing to do" not in out:
        print(f"[QEMU] dnf install toolchain failed (non-fatal): code={code}")

    code, out, err = ssh.exec(
        f"echo '{sudo_pw}' | sudo -S pip3 install --break-system-packages tmt 2>&1 | tail -30",
        timeout=1800,
    )
    if code == 0:
        code2, out2, err2 = ssh.exec("tmt --version", timeout=60)
        if code2 == 0:
            # 同上：pip 装的 tmt 也依赖 fmf，同样需要自检
            print(f"[QEMU] tmt ready (pip): {out2.strip()[:200]}, checking fmf scan...")
            probe = (
                "cd ~/openruyi-autotest && "
                "timeout 60 python3 -c \"import fmf,time;t0=time.time();"
                "t=fmf.Tree('.');print('FMF_SCAN_OK',round(time.time()-t0,1),"
                "'tests',len(t.tests))\" 2>&1 | tail -3"
            )
            pcode, pout, perr = ssh.exec(probe, timeout=120)
            if pcode == 0 and "FMF_SCAN_OK" in pout:
                print(f"[QEMU] fmf scan OK: {pout.strip()[-120:]}")
                return "tmt"
            print(f"[QEMU] fmf scan failed/timeout, tmt unusable: code={pcode} "
                  f"out={pout[-300:]!r} err={perr[-200:]!r}")
            print("[QEMU] falling back to direct beakerlib execution")

    print(f"[QEMU] pip tmt install failed: code={code}\n{out[-2000:]}\n{err[-500:]}")

    # 4. tmt 彻底不可用：退化为直接执行 beakerlib 测试脚本
    code, out, err = ssh.exec(
        "test -f /usr/share/beakerlib/beakerlib.sh && echo ok", timeout=60)
    if code == 0:
        print("[QEMU] tmt unavailable, will run tests directly with beakerlib")
        return "direct"
    print("[QEMU] beakerlib not found either, tests cannot run")
    return ""


def run_tests_direct(ssh: SSHClient, sudo_pw: str, repo_dir: str,
                     test_paths: List[str], suite_paths: List[str],
                     timeout: int = 5400) -> List[Dict]:
    """tmt 不可用时，直接在 QEMU 里以 beakerlib 方式执行测试脚本。

    对于每个测试路径（/tests/functional/pkgs/acl/test_acl_getfacl_basic 形式），
    转换为仓库内相对路径并 bash 执行其 test 脚本；用 beakerlib 的日志输出
    判断 PASS/FAIL。
    """
    results: List[Dict] = []
    # 优先执行具体用例，其次套件（套件只执行其目录下的 test.sh 若存在）
    targets = list(test_paths) + list(suite_paths)
    for target in targets:
        # /tests/functional/... -> tests/functional/...
        rel = target.lstrip("/")
        test_dir = os.path.join(repo_dir, rel)
        # 找到该目录下可执行的 test 脚本（main.fmf 里 test: 字段指向的文件）
        script_rel = None
        fmf_file = os.path.join(test_dir, "main.fmf")
        if os.path.isfile(fmf_file):
            try:
                with open(fmf_file, encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("test:"):
                            script_rel = line.split(":", 1)[1].strip().strip('"').strip("'")
                            break
            except Exception:
                pass
        if not script_rel:
            # 套件目录没有 test: 时尝试 test.sh
            for cand in ("test.sh", "runtest.sh", "test"):
                if os.path.isfile(os.path.join(test_dir, cand)):
                    script_rel = cand
                    break
        if not script_rel:
            print(f"[QEMU] direct: no test script found for {target}, skip")
            continue
        script_path = os.path.join(test_dir, script_rel)
        # 上传的仓库在 QEMU 里位于 ~/openruyi-autotest
        remote_script = os.path.join(repo_dir, rel, script_rel).replace(os.sep, "/")
        # source topology.env 提供 TEST_SERVER_* 环境变量（如 TEST_SERVER_1_PASSWORD），
        # 供 lib.sh 的 sudo dnf 使用；同时 export 兜底密码。
        cmd = (
            f"cd {os.path.dirname(remote_script)} && "
            f"set -a && . {repo_dir}/topology.env 2>/dev/null; set +a; "
            f"export TEST_SERVER_1_PASSWORD='{sudo_pw}'; "
            f"echo '{sudo_pw}' | sudo -S true && "
            f"bash {remote_script} 2>&1"
        )
        print(f"[QEMU] direct running: {cmd[:200]}...")
        code, out, err = ssh.exec(cmd, timeout=timeout)
        output = out + ("\n[stderr]\n" + err if err else "")
        # beakerlib 输出（1.30+ 带时间戳/方括号）：
        #   :: [ 15:43:03 ] :: [   PASS   ] :: message
        #   ::   RESULT: PASS
        #   ::   OVERALL RESULT: PASS
        # 以 OVERALL RESULT / RESULT 为准判断整体成败，PASS 行仅做参考。
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
        print(f"[QEMU] direct result for {target}: {status} "
              f"(final={final} pass={pass_n} fail={fail_n} exit={code})")
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
    code, out, err = ssh.exec(
        f"cat > ~/openruyi-autotest/topology.env << 'EOF'\n{content}\nEOF",
        timeout=30,
    )
    return code == 0


def run_tmt_tests(ssh: SSHClient, sudo_pw: str, test_paths: List[str],
                  suite_paths: List[str], timeout: int = 5400) -> List[Dict]:
    """执行 tmt，返回每个测试用例的结果"""
    results: List[Dict] = []

    # 构造 tmt 命令（先 suite 后 case，按路径过滤）
    targets = []
    for p in suite_paths:
        targets.append(p)
    for p in test_paths:
        targets.append(p)
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
    print(f"[QEMU] Running: {cmd[:300]}...")
    code, out, err = ssh.exec(cmd, timeout=timeout)

    output = out + ("\n[stderr]\n" + err if err else "")
    print(f"[QEMU] tmt exit={code}, output length={len(output)}")

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
            elif line.strip() and not line.strip().startswith(("discover", "provision", "prepare", "execute", "report", "plan", "summary", "1 test", "total", "output", "Result")):
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
        # 附加详细输出
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


# ============================================================
# 主流程
# ============================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="Run modified tests inside QEMU VMs")
    ap.add_argument("--vm-info", required=True, help="Path to vm_info.json")
    ap.add_argument("--repo", required=True, help="Repository root (checked out PR)")
    ap.add_argument("--requirements", required=True, help="Path to vm_requirements.json")
    ap.add_argument("--output", required=True, help="Output test_results.json path")
    args = ap.parse_args()

    with open(args.vm_info, encoding="utf-8") as f:
        vm_info = json.load(f)
    with open(args.requirements, encoding="utf-8") as f:
        req = json.load(f)

    hosts = vm_info.get("hosts", [])
    test_paths = req.get("test_paths", [])
    suite_paths = req.get("suite_paths", [])
    if not hosts:
        print("No hosts in vm_info")
        return 1

    repo_root = Path(args.repo).resolve()

    # 1. 打包仓库
    print("Packaging repository...")
    tarball = package_repo(repo_root)
    print(f"Packed: {tarball}")

    all_results: List[Dict] = []
    overall_ok = True

    for host in hosts:
        host_ip = host["host_ip"]
        ssh_user = host.get("ssh_user", "openruyi")
        ssh_pw = host.get("ssh_password", "openruyi")
        host_pw = host.get("host_ssh_password", "ISRCpassword@123")

        for qemu_port in host.get("qemu_ports", []):
            print(f"\n{'='*60}\nQEMU VM: {host_ip}:{qemu_port}\n{'='*60}")
            try:
                ssh = SSHClient(host_ip, qemu_port, ssh_user, ssh_pw)
            except Exception as e:
                print(f"SSH connect failed {host_ip}:{qemu_port}: {e}")
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
                code, out, err = ssh.exec(
                    "command -v tar >/dev/null 2>&1 || "
                    f"(echo '{ssh_pw}' | sudo -S dnf install -y tar gzip 2>&1 | tail -5)",
                    timeout=600,
                )
                if code != 0:
                    raise RuntimeError(f"ensure tar failed: {out} {err}")

                # 3. 上传并解压仓库
                remote_dir = "/home/openruyi/openruyi-autotest"
                ssh.exec(f"rm -rf {remote_dir}")
                ssh.exec("mkdir -p /home/openruyi")
                if not ssh.put_file(tarball, "/home/openruyi/repo.tar.gz"):
                    raise RuntimeError("upload repo failed")
                code, out, err = ssh.exec(
                    "cd /home/openruyi && tar xzf repo.tar.gz && rm -f repo.tar.gz", timeout=300)
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
            except Exception as e:
                print(f"Error on {host_ip}:{qemu_port}: {e}")
                for p in test_paths + suite_paths:
                    all_results.append({
                        "host_ip": host_ip, "qemu_port": qemu_port,
                        "test_path": p, "status": "error",
                        "output": str(e),
                    })
                overall_ok = False
            finally:
                ssh.close()

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

    print(f"\nSummary: {json.dumps(summary)}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
