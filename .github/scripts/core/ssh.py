# -*- coding: utf-8 -*-
"""
Unified SSH client (paramiko).

Design notes: run_tests_in_qemu.py's original SSHClient.exec returns a
(code, stdout, stderr) triple; create_server.py's SSHClient.exec returns
ExecResult. We unify on ExecResult (with code/stdout/stderr attributes)
for easy sharing between commands. To avoid breaking create_server.py
(copied verbatim), core.ssh provides an SSHClient with semantics consistent
with create_server, while adding put_file and other extension methods.
"""
from __future__ import annotations

import select
import socket
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

import paramiko


@dataclass
class ExecResult:
    """SSH command execution result."""

    code: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.code == 0

    @property
    def output(self) -> str:
        return self.stdout + ("\n[stderr]\n" + self.stderr if self.stderr else "")

    def __str__(self) -> str:  # For compatibility with create_server.py's print(result) usage
        return self.output


class SSHClient:
    """paramiko SSH client wrapper, exec returns ExecResult."""

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
        """Execute a command, returning ExecResult(code, stdout, stderr).

        On timeout (channel.settimeout expiry or caller timeout expiry), returns
        ExecResult(124, collected_output, "[timeout]"), does NOT raise an exception,
        so the upper layer (e.g. run_tests_direct) won't lose already-collected suite
        results due to a single case timeout.
        """
        transport = self.ssh.get_transport()
        if transport is None:
            return ExecResult(255, "", "SSH transport closed")
        channel = transport.open_session()
        channel.settimeout(timeout)
        try:
            channel.exec_command(cmd)
        except Exception as exc:  # noqa: BLE001
            try:
                channel.close()
            except Exception:  # noqa: BLE001
                pass
            return ExecResult(255, "", str(exc))

        stdout_buf: List[str] = []
        stderr_buf: List[str] = []
        start = time.time()
        while True:
            if time.time() - start > timeout:
                try:
                    channel.close()
                except Exception:  # noqa: BLE001
                    pass
                return ExecResult(
                    124,
                    "".join(stdout_buf),
                    "".join(stderr_buf) + "\n[timeout]",
                )
            try:
                r, _, _ = select.select([channel], [], [], 1.0)
                if channel in r:
                    try:
                        data = channel.recv(65536)
                    except socket.timeout:
                        # channel.settimeout expired: return collected output (124 = timeout)
                        try:
                            channel.close()
                        except Exception:  # noqa: BLE001
                            pass
                        return ExecResult(
                            124,
                            "".join(stdout_buf),
                            "".join(stderr_buf) + "\n[timeout]",
                        )
                    if data:
                        stdout_buf.append(data.decode("utf-8", "ignore"))
                    try:
                        err = channel.recv_stderr(65536)
                    except socket.timeout:
                        try:
                            channel.close()
                        except Exception:  # noqa: BLE001
                            pass
                        return ExecResult(
                            124,
                            "".join(stdout_buf),
                            "".join(stderr_buf) + "\n[timeout]",
                        )
                    if err:
                        stderr_buf.append(err.decode("utf-8", "ignore"))
                if channel.exit_status_ready():
                    while True:
                        r2, _, _ = select.select([channel], [], [], 0.3)
                        if channel not in r2:
                            break
                        try:
                            data = channel.recv(65536)
                        except socket.timeout:
                            break
                        if data:
                            stdout_buf.append(data.decode("utf-8", "ignore"))
                        else:
                            break
                        try:
                            err = channel.recv_stderr(65536)
                        except socket.timeout:
                            break
                        if err:
                            stderr_buf.append(err.decode("utf-8", "ignore"))
                    break
            except socket.timeout:
                # channel.settimeout expired during select or recv
                try:
                    channel.close()
                except Exception:  # noqa: BLE001
                    pass
                return ExecResult(
                    124,
                    "".join(stdout_buf),
                    "".join(stderr_buf) + "\n[timeout]",
                )
            except (EOFError, OSError) as exc:
                # Connection lost: return collected output (255 = connection error)
                try:
                    channel.close()
                except Exception:  # noqa: BLE001
                    pass
                return ExecResult(255, "".join(stdout_buf),
                                  "".join(stderr_buf) + f"\n[connection lost: {exc}]")
        try:
            code = channel.recv_exit_status()
        except (socket.timeout, EOFError, OSError) as exc:
            try:
                channel.close()
            except Exception:  # noqa: BLE001
                pass
            return ExecResult(255, "".join(stdout_buf),
                              "".join(stderr_buf) + f"\n[connection lost: {exc}]")
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
        """Safely execute a shell script: base64-encoded transfer to avoid quoting/escaping issues.

        Useful for executing multi-line scripts with single/double quotes on the remote.
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
    """Poll and wait for SSH to become reachable, returning a connected SSHClient (or None).

    Same semantics as create_server.py's wait_for_sshable, but reuses the core.ssh client,
    returning a usable connection directly on success to avoid reconnecting.
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
                pass  # Retry silently
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
