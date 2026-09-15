# -*- coding: utf-8 -*-
"""
CloudPods RISC-V QEMU Server Creator

在 CloudPods 上创建一个 x86_64 KVM 虚拟机，在上面安装 QEMU，
下载 RISC-V 固件和镜像，启动 QEMU 并等待 SSH 可达。

参考: os-autotest-runner (E:\code\mugen-generator\os-autotest-runner)
"""

import json
import logging
import os
import random
import re
import socket
import sys
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import paramiko
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# Password decryption utility
# ============================================================
import base64
import hashlib

_MASTER_KEY = "openruyi-autotest-2024-secret-key"


def _derive_key(master_key: str) -> bytes:
    """Derive a 32-byte AES-like key from master key using SHA-256."""
    return hashlib.sha256(master_key.encode()).digest()


def _decrypt_password(encrypted: str, master_key: str = _MASTER_KEY) -> str:
    """Decrypt an XOR+Base64 encrypted password back to plaintext."""
    key = _derive_key(master_key)
    encrypted_bytes = base64.b64decode(encrypted)
    decrypted = bytes(
        [encrypted_bytes[i] ^ key[i % len(key)] for i in range(len(encrypted_bytes))]
    )
    return decrypted.decode("utf-8")

# ============================================================
# Logging
# ============================================================
log = logging.getLogger("create_server")
log.setLevel(logging.DEBUG)
_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_console = logging.StreamHandler()
_console.setFormatter(_formatter)
_console.setLevel(logging.DEBUG)
log.addHandler(_console)


# ============================================================
# SSH Client (lightweight, based on os-autotest-runner SSHClient)
# ============================================================
class ExecResult:
    def __init__(self, ip: str, port: int, exit_code: int, stdout: str = "", stderr: str = ""):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        if exit_code != 0:
            log.error(f"{ip}:{port} | exit={exit_code} stdout={stdout[:200]} stderr={stderr[:200]}")
        else:
            log.info(f"{ip}:{port} | exit={exit_code} stdout={stdout[:200]}")


class SSHClient:
    """基于 paramiko 的 SSH 客户端"""

    def __init__(self, ip: str = "127.0.0.1", port: int = 22,
                 username: str = "root", password: str = "",
                 sudo_password: str = "",
                 connect_timeout: int = 10, quiet: bool = False):
        self.ip = ip
        self.port = port
        self.__username = username
        self.__password = password
        self.__sudo_password = sudo_password
        self.__connect_timeout = connect_timeout
        self.__quiet = quiet
        self.__ssh: Optional[paramiko.SSHClient] = None
        self.__connect()

    def __connect(self) -> bool:
        try:
            self.__ssh = paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh.connect(
                self.ip, port=self.port,
                username=self.__username, password=self.__password,
                look_for_keys=False, allow_agent=False,
                timeout=self.__connect_timeout,
                banner_timeout=self.__connect_timeout,
                auth_timeout=self.__connect_timeout,
            )
            if not self.__quiet:
                log.info(f"{self.ip}:{self.port} | SSH connected")
            return True
        except Exception as e:
            if not self.__quiet:
                log.warning(f"{self.ip}:{self.port} | SSH connect failed: {e}")
            return False

    def close(self):
        try:
            self.__ssh.close()
        except Exception:
            pass

    def reconnect(self) -> bool:
        self.close()
        return self.__connect()

    def exec(self, cmd: str, timeout: int = 60) -> ExecResult:
        """执行命令，返回 ExecResult（若设了 sudo_password 则自动通过管道注入密码）"""
        # 自动将 sudo xxx 转为 echo 'pw' | sudo -S xxx，避免交互式密码提示
        if self.__sudo_password and cmd.startswith("sudo "):
            cmd = f"echo '{self.__sudo_password}' | sudo -S {cmd[5:]}"

        log.info(f"{self.ip}:{self.port} | exec: {cmd[:200]}")
        try:
            transport = self.__ssh.get_transport()
            if not transport or not transport.is_active():
                log.error(f"{self.ip}:{self.port} | SSH not active")
                return ExecResult(self.ip, self.port, 255, "", "SSH not active")

            channel = transport.open_session()
            channel.exec_command(cmd)

            stdout_parts = []
            stderr_parts = []
            start = time.time()
            last_progress = start

            # select.poll() on the underlying channel fd — only way to reliably avoid
            # blocking on recv() across all paramiko versions (settimeout not reliable)
            import select as _select

            while True:
                elapsed = time.time() - start
                if elapsed > timeout:
                    log.error(f"{self.ip}:{self.port} | ⚠️ TIMEOUT after {timeout}s, closing channel ⚠️")
                    try:
                        channel.close()
                    except Exception:
                        pass
                    return ExecResult(self.ip, self.port, 124, ''.join(stdout_parts),
                                      ''.join(stderr_parts) + "\n[timeout]")

                # poll for data with 0.5s timeout (non-CPU-burning short poll)
                r, _, _ = _select.select([channel], [], [], 0.5)
                if channel in r:
                    data = channel.recv(65536)
                    if data:
                        stdout_parts.append(data.decode('utf-8', 'ignore'))
                    err_data = channel.recv_stderr(65536)
                    if err_data:
                        stderr_parts.append(err_data.decode('utf-8', 'ignore'))

                if channel.exit_status_ready():
                    # 命令已退出，排空剩余数据
                    while True:
                        r2, _, _ = _select.select([channel], [], [], 0.2)
                        if channel not in r2:
                            break
                        data = channel.recv(65536)
                        if data:
                            stdout_parts.append(data.decode('utf-8', 'ignore'))
                        else:
                            break
                        err_data = channel.recv_stderr(65536)
                        if err_data:
                            stderr_parts.append(err_data.decode('utf-8', 'ignore'))
                    break

                # 检查 transport 存活
                if not transport.is_active():
                    log.error(f"{self.ip}:{self.port} | SSH transport died during exec")
                    return ExecResult(self.ip, self.port, 255,
                                      ''.join(stdout_parts),
                                      ''.join(stderr_parts) + "\n[ssh disconnected]")

                # 长时间任务输出进度信息
                if time.time() - last_progress > 120:
                    last_progress = time.time()
                    log.info(f"{self.ip}:{self.port} | still running... ({int(elapsed)}s elapsed)")

            exit_code = channel.recv_exit_status()
            return ExecResult(self.ip, self.port, exit_code,
                              ''.join(stdout_parts), ''.join(stderr_parts))
        except Exception as e:
            log.error(f"{self.ip}:{self.port} | exec error: {e}")
            return ExecResult(self.ip, self.port, 255, "", str(e))

    def put_file(self, local_path: str, remote_path: str) -> bool:
        """上传文件到远端"""
        try:
            sftp = self.__ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            log.info(f"{self.ip}:{self.port} | uploaded {local_path} -> {remote_path}")
            return True
        except Exception as e:
            log.error(f"{self.ip}:{self.port} | upload failed: {e}")
            return False


# ============================================================
# CloudPods API Client
# ============================================================
class CloudPodsClient:
    """CloudPods REST API 客户端 (精简版)"""

    def __init__(self, keystone_url: str, username: str, password: str,
                 domain: str = "default", project: str = "system"):
        self.__keystone_url = keystone_url
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__project = project
        self.__session = self.__get_session()
        self.__endpoints = self.__get_endpoint()
        self.__compute_url = f"{self.__endpoints.get('region2', '')}/"

        self.sku = {
            1: [1, 2, 4, 8],
            2: [2, 4, 8, 12, 16],
            4: [4, 12, 16, 24, 32],
            8: [8, 16, 24, 32, 64],
            12: [12, 16, 24, 32, 64],
            16: [16, 24, 32, 48, 64],
            24: [24, 32, 48, 64, 128],
            32: [32, 48, 64, 128],
        }

    def __get_session(self) -> Optional[requests.Session]:
        session = requests.Session()
        session.headers["User-Agent"] = "yunioncloud-go/201708"
        url = f"{self.__keystone_url}/auth/tokens"
        data = {
            "auth": {
                "context": {"source": "cli"},
                "identity": {
                    "methods": ["password"],
                    "password": {"user": {"name": self.__username, "password": self.__password}},
                },
                "scope": {"project": {"domain": {"name": self.__domain}, "name": self.__project}},
            }
        }
        try:
            rs = session.post(url=url, json=data, verify=False, timeout=600)
            if rs.status_code != 200:
                log.error(f"Keystone auth failed: status={rs.status_code}, body={rs.text[:500]}")
                return None
            token = rs.headers.get("X-Subject-Token", "")
            if not token:
                log.error("Keystone auth failed: no token in response headers")
                return None
            session.headers["X-Auth-Token"] = token
            log.info(f"CloudPods session created, token={token[:20]}...")
            return session
        except Exception as e:
            log.error(f"Keystone auth error: {e}")
            return None

    def __get_endpoint(self) -> Dict[str, str]:
        try:
            url = f"{self.__keystone_url}/endpoints"
            rs = self.__session.get(url=url, verify=False, timeout=600)
            if rs.status_code != 200:
                log.warning(f"Get endpoints failed: {rs.status_code}")
                return {}
            data = rs.json()
            endpoints = {}
            for ep in data.get("endpoints", []):
                name = ep.get("service_name", "")
                ep_url = ep.get("url", "")
                if name and ep_url:
                    # Prefer IP-based endpoints over DNS names (for cross-platform compatibility)
                    if name in endpoints:
                        existing = endpoints[name]
                        # If existing is DNS and new is IP, replace
                        if not re.match(r'https?://\d+\.\d+\.\d+\.\d+', existing) and \
                           re.match(r'https?://\d+\.\d+\.\d+\.\d+', ep_url):
                            endpoints[name] = ep_url
                    else:
                        endpoints[name] = ep_url
            log.info(f"Endpoints: {list(endpoints.keys())}")
            return endpoints
        except Exception as e:
            log.error(f"Get endpoints error: {e}")
            return {}

    def _request(self, method: str, path: str, **kwargs) -> Optional[requests.Response]:
        url = f"{self.__compute_url}{path.lstrip('/')}"
        try:
            kwargs.setdefault("verify", False)
            kwargs.setdefault("timeout", 600)
            rs = self.__session.request(method, url, **kwargs)
            return rs
        except Exception as e:
            log.error(f"Request {method} {url} failed: {e}")
            return None

    def create_server_by_guest_image(
        self,
        guest_image_id: str,
        disk_image_id: str,
        arch: str,
        disk_size_mb: int = 204800,
        disks: Optional[List[int]] = None,
        nets_list: Optional[List[str]] = None,
        vm_name: str = "openruyi-autotest",
        sku: str = "ecs.g1.c4m12",
        count: int = 1,
        hypervisor: str = "kvm",
        bios: str = "BIOS",
    ) -> List[str]:
        """创建一个/多个 KVM 虚拟机，返回 server_id 列表"""
        if disks is None:
            disks = []
        if nets_list is None:
            nets_list = []

        nets = [{"network": net} for net in nets_list]

        server_config: Dict[str, Any] = {
            "auto_start": True,
            "generate_name": vm_name,
            "hypervisor": hypervisor,
            "disable_delete": False,
            "deploy_telegraf": True,
            "os_arch": arch,
            "nets": nets,
            "prefer_region": "default",
            "bios": bios,
            "guest_image_id": guest_image_id,
            "sku": sku,
            "disks": [
                {
                    "disk_type": "sys",
                    "index": 0,
                    "backend": "local",
                    "size": disk_size_mb,
                    "image_id": disk_image_id,
                    "medium": "ssd",
                }
            ],
            "reset_password": False,
        }

        for i, dsize in enumerate(disks):
            server_config["disks"].append({
                "disk_type": "data",
                "index": i + 1,
                "backend": "local",
                "size": dsize * 1024,
                "medium": "ssd",
            })

        log.info(f"Creating {count} server(s), name={vm_name}, sku={sku}, arch={arch}")
        rs = self._request("POST", "/servers", json={"count": count, "server": server_config})
        if rs is None or rs.status_code != 200:
            log.error(f"Create server failed: status={rs.status_code if rs else 'None'}")
            return []

        result = rs.json()
        server_ids = []
        if "server" in result and "id" in result["server"]:
            server_ids.append(result["server"]["id"])
        elif "servers" in result:
            for s in result["servers"]:
                sid = s.get("body", {}).get("id", "")
                if sid:
                    server_ids.append(sid)

        log.info(f"Created servers: {server_ids}")
        return server_ids

    def get_server_detail(self, server_id: str) -> Optional[Dict]:
        rs = self._request("GET", f"/servers/{server_id}")
        if rs and rs.status_code == 200:
            return rs.json()
        return None

    def get_server_ip(self, server_id: str, network_id: str = "") -> Optional[str]:
        detail = self.get_server_detail(server_id)
        if not detail:
            return None
        server = detail.get("server", {})
        nics = server.get("nics", [])
        if not nics:
            return None
        if network_id:
            for nic in nics:
                if nic.get("network_id") == network_id:
                    return nic.get("ip_addr")
            return None
        return nics[0].get("ip_addr")

    def wait_for_server_is_on(self, server_id: str, timeout: int = 1800) -> bool:
        """等待服务器进入 running 状态"""
        log.info(f"Waiting for server {server_id} to be running (timeout={timeout}s)...")
        start = time.time()
        running_count = 0
        while True:
            if time.time() - start > timeout:
                log.error(f"Timeout waiting for server {server_id}")
                return False
            detail = self.get_server_detail(server_id)
            if not detail:
                time.sleep(5)
                continue
            status = detail.get("server", {}).get("status", "")
            if "_fail" in status or status in ("disk_fail", "deploy_fail", "ready"):
                log.error(f"Server {server_id} in bad status: {status}")
                return False
            if status == "running":
                running_count += 1
                if running_count > 5:
                    log.info(f"Server {server_id} is running (confirmed {running_count} times)")
                    return True
                time.sleep(1)
            else:
                running_count = 0
                log.info(f"Server {server_id} status={status}, waiting...")
                time.sleep(5)

    def delete_server(self, server_id: str) -> bool:
        rs = self._request("DELETE", f"/servers/{server_id}")
        if rs and rs.status_code == 200:
            log.info(f"Deleted server {server_id}")
            return True
        return False

    def wait_for_server_is_deleted(self, server_id: str, timeout: int = 600) -> bool:
        log.info(f"Waiting for server {server_id} to be deleted...")
        start = time.time()
        while time.time() - start < timeout:
            detail = self.get_server_detail(server_id)
            if not detail:
                log.info(f"Server {server_id} deleted")
                return True
            time.sleep(5)
        return False


# ============================================================
# Helper functions (from os-autotest-runner)
# ============================================================
def generate_random_mac() -> str:
    parts = [random.randint(0x00, 0xFF) for _ in range(6)]
    parts[0] = (parts[0] & 0xFE) | 0x02
    return ":".join(f"{x:02x}" for x in parts)


def is_ssh_connection_lost(exit_code: int) -> bool:
    return exit_code == 255


def wait_for_sshable(ip: str, port: int, username: str, password: str,
                     timeout: int = 3600, interval: int = 10) -> bool:
    """等待 SSH 可达（直接尝试 exec，不依赖 is_sshable 独立连接）"""
    log.info(f"Waiting for {ip}:{port} SSH (timeout={timeout}s)...")
    # 抑制 paramiko 内部的 banner/连接错误日志
    paramiko_logger = logging.getLogger("paramiko")
    old_level = paramiko_logger.level
    paramiko_logger.setLevel(logging.CRITICAL)
    try:
        for i in range(0, timeout, interval):
            ssh = None
            try:
                ssh = SSHClient(ip=ip, port=port, username=username, password=password,
                                connect_timeout=10, quiet=True)
                # 直接 exec 测试；若 __connect() 失败，transport 为空，exec 返回 255
                if username == "root":
                    rs = ssh.exec("ls /", timeout=60)
                    success = rs.exit_code == 0
                else:
                    rs = ssh.exec(f"echo '{password}' | sudo -S ls /", timeout=60)
                    success = "root" in rs.stdout and rs.exit_code == 0
                if success:
                    ssh.close()
                    log.info(f"{ip}:{port} SSH OK after {i}s")
                    return True
            except Exception:
                pass  # 静默重试
            finally:
                if ssh:
                    try:
                        ssh.close()
                    except Exception:
                        pass
            time.sleep(interval)
    finally:
        paramiko_logger.setLevel(old_level)
    log.error(f"{ip}:{port} SSH timeout after {timeout}s")
    return False


def try_install_rpm(ssh: SSHClient, rpm: str, max_retries: int = 3) -> bool:
    """尝试安装 RPM 包"""
    check = ssh.exec(f"rpm -q {rpm}", timeout=60)
    if check.exit_code == 0:
        log.info(f"{ssh.ip}:{ssh.port} | {rpm} already installed")
        return True
    for i in range(max_retries):
        log.info(f"{ssh.ip}:{ssh.port} | installing {rpm} (attempt {i + 1}/{max_retries})...")
        rs = ssh.exec(
            f"sudo dnf install -y --nogpgcheck --setopt=sslverify=0 {rpm}",
            timeout=3600,
        )
        if rs.exit_code == 0:
            return True
        if "No match for argument" in rs.stdout or "No match for argument" in rs.stderr:
            log.warning(f"{ssh.ip}:{ssh.port} | {rpm} not found in repos")
            return False
        time.sleep(10)
    log.error(f"{ssh.ip}:{ssh.port} | failed to install {rpm} after {max_retries} attempts")
    return False


def try_wget(ssh: SSHClient, url: str, save_dir: str = "/opt",
             max_retries: int = 3, timeout: int = 7200) -> bool:
    """使用 wget 下载文件，带重试和进度监控"""
    filename = url.split("/")[-1]
    filepath = f"{save_dir}/{filename}"
    log.info(f"{ssh.ip}:{ssh.port} | downloading {url} -> {filepath}")

    for retry in range(max_retries):
        ssh.exec(f"sudo rm -f {filepath}")
        bg_cmd = f"cd {save_dir} && sudo wget -b -c -o {filepath}.wget-log {url}"
        ssh.exec(bg_cmd, timeout=60)

        start = time.time()
        prev_size = -1
        stable_count = 0

        while time.time() - start < timeout:
            time.sleep(10)
            rs = ssh.exec(f"sudo stat -c %s {filepath} 2>/dev/null || echo 0", timeout=60)
            size_str = rs.stdout.strip()
            current = int(size_str) if size_str.isdigit() else 0

            if current > 0:
                if current == prev_size:
                    stable_count += 1
                    if stable_count >= 5:
                        # 检查 wget 进程是否还在
                        pid_rs = ssh.exec(f"pgrep -f 'wget.*{filename}'", timeout=60)
                        if not pid_rs.stdout.strip():
                            log.info(f"{ssh.ip}:{ssh.port} | download finished (size={current})")
                            ssh.exec(f"sudo rm -f {filepath}.wget-log")
                            return True
                        else:
                            log.warning(f"{ssh.ip}:{ssh.port} | download stalled, restarting...")
                            break
                else:
                    stable_count = 0
                    elapsed = int(time.time() - start)
                    log.info(f"{ssh.ip}:{ssh.port} | downloading... {current} bytes, {elapsed}s elapsed")
                prev_size = current
            else:
                elapsed = int(time.time() - start)
                if elapsed > 60:
                    log.warning(f"{ssh.ip}:{ssh.port} | file still 0 after {elapsed}s, retrying...")
                    break

        # 清理并重试
        ssh.exec(f"sudo pkill -f 'wget.*{filename}' 2>/dev/null; sudo rm -f {filepath} {filepath}.wget-log")
        log.warning(f"{ssh.ip}:{ssh.port} | download attempt {retry + 1} failed, retrying...")
        time.sleep(20)

    log.error(f"{ssh.ip}:{ssh.port} | download failed after {max_retries} retries: {url}")
    return False


# ============================================================
# Main Logic
# ============================================================
def create_qemu_server(env: "Env") -> bool:
    """
    主要流程：
    1. 在 CloudPods 上创建 N 台 x86_64 KVM 虚拟机
    2. 等待所有虚拟机运行并获取 IP
    3. 对每台 CloudPods host：
       - 等待 SSH 可达
       - 安装 QEMU、下载 RISC-V 固件和镜像
       - 创建 bridge + TAP 设备
       - 启动 M 个 QEMU RISC-V 虚拟机
       - 等待 QEMU 内 RISC-V 虚拟机 SSH 可达
       - 配置 QEMU 虚拟网卡 (bridge IP)，使同 host 的 QEMU VM 可互通
       - 收集 bridge IP 列表
    4. 汇总输出所有 host 及其 QEMU VM 信息
    """
    # ---- Step 1: Connect to CloudPods ----
    log.info("=" * 60)
    log.info("Step 1: Connecting to CloudPods...")
    log.info("=" * 60)
    cp = CloudPodsClient(
        keystone_url=env.cloudpods_keystone_url,
        username=env.cloudpods_user,
        password=_decrypt_password(env.cloudpods_password),
    )
    if cp._CloudPodsClient__session is None:
        log.error("Failed to authenticate with CloudPods")
        return False

    # ---- Step 2: Create server(s) ----
    log.info("=" * 60)
    log.info(f"Step 2: Creating {env.cloudpods_server_num} CloudPods server(s)...")
    log.info("=" * 60)
    nets = env.cloudpods_kvm_net_list.split(",")
    # 创建虚拟机时只使用第一个网卡
    create_nets = nets[:1]
    vm_uuid = str(uuid.uuid4())
    vm_name = f"{env.server_name_prefix}-{vm_uuid.split('-', 1)[1]}"
    server_ids = cp.create_server_by_guest_image(
        guest_image_id=env.guest_image_id,
        disk_image_id=env.disk_image_id,
        arch="x86_64",
        disk_size_mb=204800,
        disks=[],
        nets_list=create_nets,
        vm_name=vm_name,
        sku=env.server_sku,
        count=env.cloudpods_server_num,
        hypervisor="kvm",
        bios=env.cloudpods_host_bios,
    )

    if not server_ids:
        log.error("Failed to create any CloudPods server")
        return False

    # ---- Step 3: Wait for all servers to be running ----
    log.info("=" * 60)
    log.info("Step 3: Waiting for servers to be running...")
    log.info("=" * 60)
    for sid in server_ids:
        if not cp.wait_for_server_is_on(sid):
            log.error(f"Server {sid} failed to start")
            # Cleanup
            for s in server_ids:
                cp.delete_server(s)
            return False

    # ---- Step 4: Get server IPs ----
    log.info("=" * 60)
    log.info("Step 4: Getting server IPs...")
    log.info("=" * 60)
    first_net = nets[0] if nets else ""
    server_ips = []
    for sid in server_ids:
        ip = cp.get_server_ip(sid, first_net)
        if not ip:
            log.error(f"Failed to get IP for server {sid}")
            for s in server_ids:
                cp.delete_server(s)
            return False
        server_ips.append(ip)
        log.info(f"Server {sid} -> {ip}")

    # ---- Step 5-14: Setup each CloudPods host ----
    all_qemu_ips: Dict[str, List[str]] = {}  # host_ip -> [bridge_ip1, ...]

    for host_idx, host_ip in enumerate(server_ips):
        log.info("=" * 60)
        log.info(f">>> Setting up host {host_idx + 1}/{len(server_ips)}: {host_ip} <<<")
        log.info("=" * 60)

        # ---- Step 5: Wait for server SSH ----
        log.info(f"[Host {host_idx}] Step 5: Waiting for server SSH...")
        if not wait_for_sshable(host_ip, 22, env.cloudpods_server_user, env.cloudpods_server_password):
            log.error(f"[Host {host_idx}] Server {host_ip} SSH not reachable")
            return False

        host_ssh = SSHClient(ip=host_ip, port=22,
                             username=env.cloudpods_server_user, password=env.cloudpods_server_password)

        # ---- Step 6: Add ISCAS mirror repo (non-destructive) & install packages ----
        log.info(f"[Host {host_idx}] Step 6: Adding ISCAS mirror repo & installing packages...")
        if env.delete_default_yum_repos.lower() == "yes":
            # 非破坏性方式：新增 ISCAS 镜像源 repo 文件，优先级高于原始仓库。
            # 如果 ISCAS 不可达，dnf 会自动使用原始 repo.openeuler.org 作为回退。
            # 不再使用 sed 破坏性替换原始 repo 文件。
            host_ssh.exec("sudo tee /etc/yum.repos.d/iscas-mirror.repo > /dev/null << 'ISCAEOF'\n"
                "[iscas-OS]\n"
                "name=ISCAS Mirror - OS\n"
                "baseurl=https://mirrors.iscas.ac.cn/openeuler/openEuler-24.03-LTS-SP2/OS/$basearch/\n"
                "enabled=1\n"
                "gpgcheck=0\n"
                "priority=1\n"
                "skip_if_unavailable=1\n"
                "\n"
                "[iscas-everything]\n"
                "name=ISCAS Mirror - Everything\n"
                "baseurl=https://mirrors.iscas.ac.cn/openeuler/openEuler-24.03-LTS-SP2/everything/$basearch/\n"
                "enabled=1\n"
                "gpgcheck=0\n"
                "priority=1\n"
                "skip_if_unavailable=1\n"
                "\n"
                "[iscas-EPOL]\n"
                "name=ISCAS Mirror - EPOL\n"
                "baseurl=https://mirrors.iscas.ac.cn/openeuler/openEuler-24.03-LTS-SP2/EPOL/$basearch/\n"
                "enabled=1\n"
                "gpgcheck=0\n"
                "priority=1\n"
                "skip_if_unavailable=1\n"
                "\n"
                "[iscas-update]\n"
                "name=ISCAS Mirror - Update\n"
                "baseurl=https://mirrors.iscas.ac.cn/openeuler/openEuler-24.03-LTS-SP2/update/$basearch/\n"
                "enabled=1\n"
                "gpgcheck=0\n"
                "priority=1\n"
                "skip_if_unavailable=1\n"
                "ISCAEOF", timeout=60)
            # 注释掉 openEuler.repo 中的 metalink= 行，因为 mirrors.openeuler.org
            # 在某些网络环境下不可达，dnf 等待 metalink 超时会导致安装极慢（每个 repo ~60s）。
            # baseurl (repo.openeuler.org) 和 ISCAS mirror 均可正常访问。
            host_ssh.exec("sudo sed -i '/^metalink=/s/^/#/' /etc/yum.repos.d/openEuler.repo", timeout=30)
            host_ssh.exec("sudo dnf clean all", timeout=3600)
            host_ssh.exec("sudo dnf makecache", timeout=600)
        required_packages = [
            "wget", "xz", "zstd", "screen", "expect",
            "firewalld", "qemu-img", "bridge-utils",
        ]
        for pkg in required_packages:
            if not try_install_rpm(host_ssh, pkg):
                log.error(f"[Host {host_idx}] Failed to install {pkg}")
                return False

        # Start firewalld
        host_ssh.exec("sudo systemctl start firewalld")
        host_ssh.exec("sudo systemctl enable firewalld")

        # ---- Step 7: Install QEMU ----
        log.info(f"[Host {host_idx}] Step 7: Installing QEMU...")
        if env.os_version in ["openRuyi-RVA23"]:
            # Install from Nexus repo
            if not try_install_rpm(host_ssh, "libslirp-devel"):
                log.error(f"[Host {host_idx}] Failed to install libslirp-devel")
                return False
            nexus_repo = """[nexus-qemu]
name=Nexus QEMU Repo
baseurl=https://nexus.gray.oepkgs.net/repository/yum-hosted/
enabled=1
gpgcheck=0
priority=1"""
            host_ssh.exec(f"sudo tee /etc/yum.repos.d/nexus-qemu.repo <<'EOF'\n{nexus_repo}\nEOF")
            host_ssh.exec("sudo yum clean all", timeout=60)
            host_ssh.exec("sudo rm -rf /var/cache/yum")
            rs = host_ssh.exec(
                "sudo yum install -y qemu-10.1.2 --disablerepo=* --enablerepo=nexus-qemu",
                timeout=180,
            )
            if rs.exit_code != 0:
                log.error(f"[Host {host_idx}] QEMU install failed: {rs.stderr[:500]}")
                return False
        else:
            # Try system QEMU
            if not try_install_rpm(host_ssh, "qemu-system-riscv"):
                log.error(f"[Host {host_idx}] Failed to install qemu-system-riscv")
                return False

        # Verify QEMU
        qemu_path = "/usr/local/qemu/bin/qemu-system-riscv64" if env.os_version in ["openRuyi-RVA23"] else "qemu-system-riscv64"
        rs = host_ssh.exec(f"{qemu_path} --version", timeout=60)
        if rs.exit_code != 0:
            log.error(f"[Host {host_idx}] QEMU version check failed: {rs.stderr[:500]}")
            return False
        log.info(f"[Host {host_idx}] QEMU version: {rs.stdout.strip()[:200]}")

        # ---- Step 8: Configure firewall ----
        log.info(f"[Host {host_idx}] Step 8: Configuring firewall ports...")
        for port in [f"{12055 + i}/tcp" for i in range(env.riscv_qemu_num)]:
            check = host_ssh.exec(f"sudo firewall-cmd --zone=public --query-port={port} --permanent", timeout=60)
            if check.exit_code != 0:
                rs = host_ssh.exec(f"sudo firewall-cmd --zone=public --add-port={port} --permanent", timeout=60)
                if rs.exit_code != 0:
                    log.warning(f"[Host {host_idx}] Failed to add firewall port {port}: {rs.stderr}")
        host_ssh.exec("sudo firewall-cmd --reload", timeout=60)

        # ---- Step 9: Download RISC-V image & firmware ----
        log.info(f"[Host {host_idx}] Step 9: Downloading RISC-V image and firmware...")
        host_ssh.exec("sudo rm -rf /opt/*.xz /opt/*.zst /opt/*.fd /opt/*.qcow2 2>/dev/null")

        if not try_wget(host_ssh, env.riscv_image_url, "/opt"):
            log.error(f"[Host {host_idx}] Failed to download RISC-V image")
            return False
        if not try_wget(host_ssh, env.riscv_virt_code_url, "/opt"):
            log.error(f"[Host {host_idx}] Failed to download RISCV_VIRT_CODE.fd")
            return False
        if not try_wget(host_ssh, env.riscv_virt_vars_url, "/opt"):
            log.error(f"[Host {host_idx}] Failed to download RISCV_VIRT_VARS.fd")
            return False

        # ---- Step 10: Decompress image ----
        log.info(f"[Host {host_idx}] Step 10: Decompressing RISC-V image...")
        image_name = env.riscv_image_url.split("/")[-1]
        if ".qcow2.xz" in image_name:
            rs = host_ssh.exec("cd /opt && sudo xz -d -f *.qcow2.xz", timeout=3600)
            if rs.exit_code != 0:
                log.error(f"[Host {host_idx}] xz decompress failed: {rs.stderr}")
                return False
            image_name = image_name.replace(".qcow2.xz", ".qcow2")
        elif ".qcow2.zst" in image_name:
            rs = host_ssh.exec("cd /opt && sudo zstd -d -f *.qcow2.zst", timeout=3600)
            if rs.exit_code != 0:
                log.error(f"[Host {host_idx}] zstd decompress failed: {rs.stderr}")
                return False
            image_name = image_name.replace(".qcow2.zst", ".qcow2")
        log.info(f"[Host {host_idx}] Image decompressed: {image_name}")

        virt_code_name = env.riscv_virt_code_url.split("/")[-1]
        virt_vars_name = env.riscv_virt_vars_url.split("/")[-1]

        # 保留原始 VARS 模板副本（每个 VM 需要独立的 VARS 文件，否则 UEFI 变量冲突导致无法启动）
        host_ssh.exec(f"sudo cp /opt/{virt_vars_name} /opt/{virt_vars_name}.template")

        # ---- Step 11: Create bridge and TAP devices ----
        log.info(f"[Host {host_idx}] Step 11: Setting up bridge and TAP devices...")

        # Create bridge br0
        host_ssh.exec("sudo brctl addbr br0")
        time.sleep(3)
        host_ssh.exec("sudo ip link set br0 up")
        time.sleep(3)
        ip_check = host_ssh.exec("sudo ip addr show dev br0", timeout=60)
        if "10.0.0.1/24" not in ip_check.stdout:
            rs = host_ssh.exec("sudo ip addr add 10.0.0.1/24 dev br0", timeout=60)
            if rs.exit_code != 0:
                log.error(f"[Host {host_idx}] Failed to add IP to br0: {rs.stderr}")
                return False

        # Enable IP forwarding & NAT
        host_ssh.exec('sudo sh -c \'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf\' && sudo sysctl -p')
        host_ssh.exec("sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE")

        # Determine per-QEMU CPU/Memory from env (no longer dividing SKU by qemu_num)
        qemu_cpu = env.riscv_qemu_cpu
        qemu_memory = env.riscv_qemu_memory
        required_cpu = qemu_cpu * env.riscv_qemu_num
        required_memory = qemu_memory * env.riscv_qemu_num

        # Validate SKU can support the total resource requirement
        sku_match = re.search(r"ecs\.g1\.c(\d+)m(\d+)", env.server_sku)
        if sku_match:
            sku_cpu = int(sku_match.group(1))
            sku_mem = int(sku_match.group(2))
            if sku_cpu < required_cpu:
                log.warning(
                    f"[Host {host_idx}] SKU {env.server_sku} has {sku_cpu}C, "
                    f"but {env.riscv_qemu_num} QEMU VMs need {required_cpu}C total. "
                    f"Consider using a larger SKU."
                )
            if sku_mem < required_memory:
                log.warning(
                    f"[Host {host_idx}] SKU {env.server_sku} has {sku_mem}G, "
                    f"but {env.riscv_qemu_num} QEMU VMs need {required_memory}G total. "
                    f"Consider using a larger SKU."
                )

        # Parse disks
        if env.riscv_qemu_disks:
            try:
                disk_sizes = json.loads(env.riscv_qemu_disks)
            except json.JSONDecodeError:
                disk_sizes = []
                log.warning(f"[Host {host_idx}] Failed to parse RISCV_QEMU_DISKS='{env.riscv_qemu_disks}', using empty list")
        else:
            disk_sizes = []

        # ---- Step 12: Launch QEMU VMs ----
        log.info(f"[Host {host_idx}] Step 12: Launching {env.riscv_qemu_num} QEMU VM(s)...")
        log.info(f"  Per-QEMU: CPU={qemu_cpu}, Memory={qemu_memory}G, NICs={env.riscv_qemu_net_num}, Disks={disk_sizes}")
        log.info(f"  Total required: {qemu_cpu * env.riscv_qemu_num}C / {qemu_memory * env.riscv_qemu_num}G, SKU={env.server_sku}")

        for i in range(env.riscv_qemu_num):
            # 每个 VM 需要独立的 UEFI VARS 文件（可读写），共享会导致 UEFI 变量损坏
            per_vm_vars = f"RISCV_VIRT_VARS_{i}.fd"
            host_ssh.exec(f"sudo cp /opt/{virt_vars_name}.template /opt/{per_vm_vars}")

            # Create base qcow2
            base_name = f"riscv-mugen-server-{i}.qcow2"
            cmd = f"cd /opt && sudo qemu-img create -f qcow2 -F qcow2 -b {image_name} {base_name}"
            rs = host_ssh.exec(cmd, timeout=3600)
            if rs.exit_code != 0:
                log.error(f"[Host {host_idx}] QEMU {i}: Failed to create qcow2: {rs.stderr}")
                return False
            time.sleep(3)

            # Create extra disks
            disk_names = []
            for j, dsize in enumerate(disk_sizes):
                dname = f"disk{i}{j}.qcow2"
                cmd = f"cd /opt && sudo qemu-img create -f qcow2 {dname} {dsize}G"
                rs = host_ssh.exec(cmd, timeout=1800)
                if rs.exit_code != 0:
                    log.error(f"[Host {host_idx}] QEMU {i}: Failed to create extra disk {dname}: {rs.stderr}")
                    return False
                time.sleep(3)
                disk_names.append(dname)

            # Create TAP devices
            total_nics = env.riscv_qemu_net_num + 1  # +1 for management
            for j in range(total_nics):
                tap_name = f"tap{i * total_nics + j}"
                # Check if tap exists
                rs = host_ssh.exec(f"sudo ip link show {tap_name}", timeout=60)
                if rs.exit_code != 0:
                    host_ssh.exec(f"sudo ip tuntap add {tap_name} mode tap")
                time.sleep(3)
                # Add to bridge
                check = host_ssh.exec(f"sudo brctl show br0 | grep -w {tap_name}", timeout=60)
                if check.exit_code != 0:
                    host_ssh.exec(f"sudo brctl addif br0 {tap_name}")
                time.sleep(3)
                # Set up
                check = host_ssh.exec(f"sudo ip link show {tap_name} | grep -w UP", timeout=60)
                if check.exit_code != 0:
                    host_ssh.exec(f"sudo ip link set {tap_name} up")
                time.sleep(3)

            # Build QEMU command
            if env.os_version in ["openRuyi-RVA23"]:
                qemu_cmd = "cd /opt && /usr/local/qemu/bin/qemu-system-riscv64"
            else:
                qemu_cmd = "cd /opt && qemu-system-riscv64"

            qemu_cmd += " -nographic"
            qemu_cmd += " -machine virt,pflash0=pflash0,pflash1=pflash1"
            qemu_cmd += f" -smp {qemu_cpu} -m {qemu_memory}G"
            qemu_cmd += " -rtc base=utc,clock=host"

            # BIOS: uefi with pflash
            qemu_cmd += f" -blockdev node-name=pflash0,driver=file,read-only=on,filename={virt_code_name}"
            qemu_cmd += f" -blockdev node-name=pflash1,driver=file,filename={per_vm_vars}"
            qemu_cmd += " -cpu rva23s64"

            # System disk
            qemu_cmd += f" -drive file={base_name},format=qcow2,id=hd0,if=none"
            qemu_cmd += " -object rng-random,filename=/dev/urandom,id=rng0"
            qemu_cmd += " -device virtio-vga"
            qemu_cmd += " -device virtio-rng-device,rng=rng0"
            qemu_cmd += " -device virtio-blk-device,drive=hd0"
            qemu_cmd += " -device qemu-xhci -usb -device usb-kbd -device usb-tablet"

            # Extra data disks
            for j, dname in enumerate(disk_names):
                qemu_cmd += f" -drive file={dname},format=qcow2,id=hd{j + 1},if=none"
                qemu_cmd += f" -device virtio-blk-pci,drive=hd{j + 1}"

            # NICs through bridge
            for j in range(env.riscv_qemu_net_num + 1):
                tap_idx = i * total_nics + j
                mac = generate_random_mac()
                qemu_cmd += f" -netdev tap,id=net{tap_idx},ifname=tap{tap_idx},script=no,downscript=no"
                qemu_cmd += f" -device virtio-net-pci,netdev=net{tap_idx},mac={mac}"

            # User-mode NIC with hostfwd for SSH
            mac = generate_random_mac()
            qemu_cmd += f" -netdev user,id=usernet,hostfwd=tcp::{12055 + i}-:22"
            qemu_cmd += f" -device virtio-net-pci,netdev=usernet,mac={mac}"

            # Write QEMU command to a script and start via screen
            script_path = f"/opt/start_qemu_{i}.sh"
            host_ssh.exec(f"cat > {script_path} << 'QEMUEOF'\n{qemu_cmd}\nQEMUEOF")

            screen_name = f"qemu-{i}"
            # Kill existing screen session if any
            host_ssh.exec(f"sudo screen -S {screen_name} -X quit 2>/dev/null")
            time.sleep(2)
            host_ssh.exec(
                f"cd /opt && sudo screen -S {screen_name} -d -m bash {script_path}",
                timeout=60,
            )
            log.info(f"[Host {host_idx}] QEMU {i}: screen session '{screen_name}' started")
            time.sleep(15)

        # ---- Step 13: Wait for QEMU SSH ----
        log.info(f"[Host {host_idx}] Step 13: Waiting for {env.riscv_qemu_num} QEMU VM(s) to be SSHable...")
        log.info(f"  Host: {host_ip}, Ports: {[12055 + i for i in range(env.riscv_qemu_num)]}")
        log.info(f"  User: {env.riscv_default_username}, Password: {env.riscv_default_password}")

        for i in range(env.riscv_qemu_num):
            qemu_port = 12055 + i
            if not wait_for_sshable(
                ip=host_ip,
                port=qemu_port,
                username=env.riscv_default_username,
                password=env.riscv_default_password,
                timeout=env.testsuite_max_timeout,
            ):
                log.error(f"[Host {host_idx}] QEMU VM {i} (port {qemu_port}) SSH not reachable")
                return False
            log.info(f"[Host {host_idx}] QEMU VM {i}: SSH reachable at {host_ip}:{qemu_port} ✅")

        # ---- Step 14: Configure QEMU guest networking ----
        log.info(f"[Host {host_idx}] Step 14: Configuring QEMU guest networking...")
        host_qemu_ips: List[str] = []

        for i in range(env.riscv_qemu_num):
            qemu_port = 12055 + i
            vm_ssh = SSHClient(
                ip=host_ip, port=qemu_port,
                username=env.riscv_default_username,
                password=env.riscv_default_password,
                sudo_password=env.riscv_default_password,
            )

            # Configure yum repos inside guest
            if env.delete_default_yum_repos.lower() == "yes":
                # 注释掉 metalink，强制走 baseurl；使用通配符适配镜像的 repo 文件名
                vm_ssh.exec("sudo sed -i 's/^metalink=/#metalink=/g' /etc/yum.repos.d/*.repo")
                vm_ssh.exec("sudo sed -i 's/^#metalink=/metalink=/g' /etc/yum.repos.d/*.repo")  # 取消已注释的
                vm_ssh.exec("sudo sed -i 's/metalink=/#metalink=/g' /etc/yum.repos.d/*.repo")
            if env.add_yum_repos:
                for idx, repo_url in enumerate(env.add_yum_repos.split(",")):
                    repo_content = f"""[local-{idx}]
name=local-{idx}
baseurl={repo_url}
priority=10
enabled=1
gpgcheck=0
skip_if_unavailable=1"""
                    vm_ssh.exec(f"sudo tee /etc/yum.repos.d/local-{idx}.repo <<'EOF'\n{repo_content}\nEOF")
                vm_ssh.exec("sudo dnf clean all", timeout=3600)
                vm_ssh.exec("sudo dnf makecache", timeout=600)

            # Time sync
            try_install_rpm(vm_ssh, "ntpdate")
            vm_ssh.exec("sudo ntpdate cn.pool.ntp.org", timeout=3600)
            vm_ssh.exec("sudo timedatectl set-timezone Asia/Shanghai")

            # Configure virtual NICs
            try_install_rpm(vm_ssh, "lshw")
            try_install_rpm(vm_ssh, "net-tools")

            output = vm_ssh.exec(
                "sudo lshw -class network | grep -A 5 'description: Ethernet interface' | "
                "grep 'logical name:' | awk '{print $NF}' | grep -v 'lo'",
                timeout=3600,
            ).stdout
            nic_names = [n.strip() for n in output.strip().split("\n") if n.strip()]
            log.info(f"[Host {host_idx}] QEMU VM {i}: NIC names = {nic_names}")

            nmcli_check = vm_ssh.exec("sudo nmcli --version", timeout=60)
            has_nmcli = "command not found" not in nmcli_check.stdout and "command not found" not in nmcli_check.stderr

            if has_nmcli:
                for j in range(min(len(nic_names), env.riscv_qemu_net_num + 1)):
                    if not nic_names[j]:
                        continue
                    vm_ssh.exec(f"sudo nmcli c a type Ethernet con-name {nic_names[j]} ifname {nic_names[j]}")
                    time.sleep(5)
                    vm_ssh.exec(f"sudo nmcli c m {nic_names[j]} ipv4.address 10.0.0.{i + 1}{j}/24")
                    time.sleep(5)
                    vm_ssh.exec(f"sudo nmcli c m {nic_names[j]} ipv4.method manual")
                    time.sleep(5)
                    vm_ssh.exec(f"sudo nmcli c up {nic_names[j]}")
                    time.sleep(10)

            # Collect bridge IP
            nic_ip = vm_ssh.exec(
                "sudo ip -4 a | grep '10\\.0\\.' | awk '{print $2}' | head -n 1 | awk -F '/' '{print $1}'",
                timeout=60,
            ).stdout.strip()
            if nic_ip.startswith("10.0."):
                host_qemu_ips.append(nic_ip)
                log.info(f"[Host {host_idx}] QEMU VM {i}: bridge IP = {nic_ip}")
            else:
                log.warning(f"[Host {host_idx}] QEMU VM {i}: failed to get bridge IP, got: {nic_ip}")

            vm_ssh.close()

        all_qemu_ips[host_ip] = host_qemu_ips
        log.info(f"[Host {host_idx}] Host setup complete. QEMU bridge IPs: {host_qemu_ips}")

    # ---- Done ----
    log.info("=" * 60)
    log.info("ALL DONE! ✅")
    log.info(f"CloudPods Server ID(s): {server_ids}")
    log.info(f"Total {len(server_ips)} host(s), {len(server_ips) * env.riscv_qemu_num} QEMU VM(s)")
    for host_idx, host_ip in enumerate(server_ips):
        log.info(f"--- Host {host_idx}: {host_ip} ---")
        for i in range(env.riscv_qemu_num):
            log.info(f"  QEMU VM {i}: ssh -p {12055 + i} {env.riscv_default_username}@{host_ip}")
        bridge_ips = all_qemu_ips.get(host_ip, [])
        if bridge_ips:
            log.info(f"  Bridge IPs (for inter-QEMU SSH on this host): {', '.join(bridge_ips)}")
    log.info("=" * 60)
    return True


# ============================================================
# Env Configuration Class
# ============================================================
class Env:
    """配置类 —— 修改这里的变量来适配不同环境"""

    # ---- CloudPods 连接 ----
    cloudpods_keystone_url: str = "https://10.20.40.101:30500/v3"
    cloudpods_user: str = "admin"
    cloudpods_password: str = "0Ub4/mK058E="

    # ---- CloudPods 虚拟机规格 ----
    os_version: str = "openRuyi-RVA23"
    os_arch: str = "riscv64"
    guest_image_id: str = "6f59c2c8-73f8-449b-8546-b6cf2b5564a0"
    disk_image_id: str = "40fb8262-0566-4877-8eb0-d991903e9be7"
    cloudpods_host_bios: str = "BIOS"
    server_name_prefix: str = "redrose2100"
    server_sku: str = "ecs.g1.c16m16"
    cloudpods_kvm_net_list: str = (
        "efdb73ac-d785-47a1-82bf-65c2229eacca,"
        "3e0ac273-6da8-4188-821b-d97a84cb7754,"
        "04bc4008-f5a6-40a0-84aa-5fcd76e3f2ef,"
        "0f71d7ea-6e7a-42bc-81c3-290e396581a7,"
        "b7272573-29ea-4e46-8c27-22b81503aee6"
    )

    # ---- 虚拟机 SSH 凭据 ----
    cloudpods_server_user: str = "root"
    cloudpods_server_password: str = "ISRCpassword@123"

    # ---- YUM 源 ----
    delete_default_yum_repos: str = "yes"
    add_yum_repos: str = "https://diamond.oerv.ac.cn/openruyi/riscv64/"

    # ---- RISC-V QEMU 资源 ----
    riscv_bios: str = "uefi"
    riscv_default_username: str = "openruyi"
    riscv_default_password: str = "openruyi"
    riscv_image_url: str = "https://s3.develop.oepkgs.net/demo/openruyi-virt_riscv64.qcow2.xz"
    riscv_virt_code_url: str = "https://s3.develop.oepkgs.net/demo/RISCV_VIRT_CODE.fd"
    riscv_virt_vars_url: str = "https://s3.develop.oepkgs.net/demo/RISCV_VIRT_VARS.fd"

    # ---- 新增变量 ----
    cloudpods_server_num: int = 1       # CloudPods 虚拟机的数量
    riscv_qemu_num: int = 2             # QEMU 中 RISC-V 虚拟机的数量
    riscv_qemu_cpu: int = 8             # 每个 QEMU VM 分配的 CPU 核数
    riscv_qemu_memory: int = 8          # 每个 QEMU VM 分配的内存（GB）
    riscv_qemu_net_num: int = 1         # 每个 QEMU VM 需要的额外网卡数量（默认 1）
    riscv_qemu_disks: str = ""          # 额外磁盘列表，JSON 格式，如 '[20,20]'（默认空 = 不额外增加）

    # ---- 超时 ----
    testsuite_max_timeout: int = 10800  # QEMU SSH 等待超时（秒）


# ============================================================
# Entry Point
# ============================================================
if __name__ == "__main__":
    env = Env()
    success = create_qemu_server(env)
    sys.exit(0 if success else 1)
