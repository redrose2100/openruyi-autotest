# -*- coding: utf-8 -*-
"""
统一 SSH 客户端（paramiko）。

设计说明：run_tests_in_qemu.py 原来的 SSHClient.exec 返回 (code, stdout, stderr)
三元组；create_server.py 的 SSHClient.exec 返回 ExecResult。这里统一为
ExecResult（含 code/stdout/stderr 属性），便于命令间共享。为避免破坏
create_server.py（原样复制），core.ssh 提供与 create_server 一致语义的
SSHClient，同时新增 put_file 等扩展方法。
"""
from __future__ import annotations

import select
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

import paramiko


@dataclass
class ExecResult:
    """SSH 命令执行结果。"""

    code: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.code == 0

    @property
    def output(self) -> str:
        return self.stdout + ("\n[stderr]\n" + self.stderr if self.stderr else "")

    def __str__(self) -> str:  # 兼容 create_server.py 的 print(result) 用法
        return self.output


class SSHClient:
    """paramiko SSH 客户端封装，exec 返回 ExecResult。"""

    def __init__(
        self,
        ip: str,
        port: int,
        username: str,
        password: str,
        connect_timeout: int = 20,
    ):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            ip,
            port=port,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
            timeout=connect_timeout,
            banner_timeout=connect_timeout,
            auth_timeout=connect_timeout,
        )

    def exec(self, cmd: str, timeout: int = 600) -> ExecResult:
        """执行命令，返回 ExecResult(code, stdout, stderr)。"""
        transport = self.ssh.get_transport()
        channel = transport.open_session()
        channel.settimeout(timeout)
        try:
            channel.exec_command(cmd)
        except Exception as exc:  # noqa: BLE001
            return ExecResult(255, "", str(exc))

        stdout_buf: List[str] = []
        stderr_buf: List[str] = []
        start = time.time()
        while True:
            if time.time() - start > timeout:
                channel.close()
                return ExecResult(
                    124,
                    "".join(stdout_buf),
                    "".join(stderr_buf) + "\n[timeout]",
                )
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
                    else:
                        break
                    err = channel.recv_stderr(65536)
                    if err:
                        stderr_buf.append(err.decode("utf-8", "ignore"))
                break
        code = channel.recv_exit_status()
        return ExecResult(code, "".join(stdout_buf), "".join(stderr_buf))

    def put_file(self, local: str, remote: str) -> bool:
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(local, remote)
            sftp.close()
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"[SSH] upload failed {local} -> {remote}: {exc}")
            return False

    def exec_script(self, script: str, timeout: int = 120) -> ExecResult:
        """安全执行一段 shell 脚本：base64 编码传输，规避引号/转义问题。

        适用于需要在远端执行多行、含单双引号的脚本场景。
        """
        import base64

        encoded = base64.b64encode(script.encode("utf-8")).decode("ascii")
        return self.exec(
            f"sudo bash -c \"echo '{encoded}' | base64 -d > /tmp/_ci_script.sh "
            f"&& bash /tmp/_ci_script.sh; rm -f /tmp/_ci_script.sh\"",
            timeout=timeout,
        )

    def close(self) -> None:
        try:
            self.ssh.close()
        except Exception:  # noqa: BLE001
            pass


def wait_ssh_ready(
    ip: str,
    port: int,
    username: str,
    password: str,
    timeout: int = 3600,
    interval: int = 10,
    connect_timeout: int = 10,
    quiet: bool = True,
) -> Optional[SSHClient]:
    """轮询等待 SSH 可达，返回已连接的 SSHClient（或 None）。

    与 create_server.py 的 wait_for_sshable 语义一致，但复用 core.ssh 客户端，
    成功时直接返回可用的连接，避免重复连接。
    """
    import logging
    import time

    logger = logging.getLogger("ci_cli.ssh")
    logger.info("Waiting for %s:%s SSH (timeout=%ss)...", ip, port, timeout)

    paramiko_logger = logging.getLogger("paramiko")
    old_level = paramiko_logger.level
    paramiko_logger.setLevel(logging.CRITICAL)
    try:
        for i in range(0, timeout, interval):
            ssh: Optional[SSHClient] = None
            try:
                ssh = SSHClient(
                    ip=ip,
                    port=port,
                    username=username,
                    password=password,
                    connect_timeout=connect_timeout,
                )
                rs = ssh.exec("echo SSH_OK", timeout=60)
                if rs.code == 0:
                    logger.info("%s:%s SSH OK after %ss", ip, port, i)
                    return ssh
            except Exception:  # noqa: BLE001
                pass  # 静默重试
            finally:
                if ssh is not None:
                    try:
                        ssh.close()
                    except Exception:  # noqa: BLE001
                        pass
            time.sleep(interval)
    finally:
        paramiko_logger.setLevel(old_level)
    logger.error("%s:%s SSH timeout after %ss", ip, port, timeout)
    return None
