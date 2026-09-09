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
                while True:
                    r2, _, _ = select.select([channel], [], [], 0.3)
                    if channel not in r2:
                        break
                    data = channel.recv(65536)
                    if data:
                        stdout_buf.append(data.decode("utf-8", "ignore"))
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

def remote_prepare_env(ssh: SSHClient, sudo_pw: str) -> bool:
    """在 QEMU 中安装 tmt + beakerlib"""
    # 确保 sudo 免密可用
    ssh.exec(f"echo '{sudo_pw}' | sudo -S true")
    # 安装 pip 与 beakerlib
    code, out, err = ssh.exec(
        f"echo '{sudo_pw}' | sudo -S dnf install -y python3-pip beakerlib python-six 2>&1 | tail -20",
        timeout=1800,
    )
    if code != 0 and "Nothing to do" not in out:
        print(f"[QEMU] dnf install python3-pip beakerlib failed: code={code}\n{out}\n{err}")
        return False

    # 安装 tmt（riscv64 仓库可能没有，用 pip）
    code, out, err = ssh.exec(
        "tmt --version 2>/dev/null || pip3 install --break-system-packages tmt 2>&1 | tail -5",
        timeout=900,
    )
    if code != 0:
        print(f"[QEMU] tmt install failed: code={code}\n{out}\n{err}")
        return False
    print(f"[QEMU] tmt ready: {out.strip()[:200]}")
    return True


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
        f"tmt run --all plan --name /plans/functional {name_args} "
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
                # 2. 上传并解压仓库
                remote_dir = "/home/openruyi/openruyi-autotest"
                ssh.exec(f"rm -rf {remote_dir}")
                ssh.exec("mkdir -p /home/openruyi")
                if not ssh.put_file(tarball, "/home/openruyi/repo.tar.gz"):
                    raise RuntimeError("upload repo failed")
                code, out, err = ssh.exec(
                    "cd /home/openruyi && tar xzf repo.tar.gz && rm -f repo.tar.gz", timeout=300)
                if code != 0:
                    raise RuntimeError(f"extract failed: {out} {err}")

                # 3. 准备环境（tmt/beakerlib）
                if not remote_prepare_env(ssh, ssh_pw):
                    raise RuntimeError("prepare env failed")

                # 4. 配置 topology.env
                remote_setup_topology(ssh, ssh_pw, host_ip)

                # 5. 运行 tmt
                vm_results = run_tmt_tests(ssh, ssh_pw, test_paths, suite_paths)
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
