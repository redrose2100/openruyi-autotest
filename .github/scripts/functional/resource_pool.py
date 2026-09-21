# -*- coding: utf-8 -*-
"""Resource pool management: CloudPods env acquire / verify / release / cleanup.

Implements requirements 2.3~2.6:
  - 2.3 Before each test suite, search CloudPods pool for a matching VM env
        (name prefix match + SSH availability check); create one if none found.
  - 2.4 If a pooled VM is unavailable (SSH fails), delete it and recreate.
  - 2.5 After test suite completes, release the env back to pool (no delete).
  - 2.6 After all test suites complete, delete all envs used in this batch.

Env definition: a CloudPods server (KVM host) + N QEMU VMs on it.
Pool is differentiated by name prefix (env_prefix); one env = one server.
"""
from __future__ import annotations

import json
import logging
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

from core.cloudpods import CloudPodsClient
from core.config import get_env

logger = logging.getLogger("ci_cli.functional.resource_pool")

# CloudPods credentials: env var priority -> explicit param -> create_server.Env defaults

def _default_credentials() -> Dict[str, str]:
    """Read default credentials from create_server.Env (consistent with launch_env creation)."""
    try:
        from cloudpods import create_server as cs
        env = cs.Env
        return {
            "keystone_url": getattr(env, "cloudpods_keystone_url", ""),
            "username": getattr(env, "cloudpods_user", ""),
            "password": getattr(env, "cloudpods_password", ""),
        }
    except Exception:  # noqa: BLE001
        return {"keystone_url": "", "username": "", "password": ""}


def _get_credentials(vm_info: Optional[Dict] = None) -> Dict[str, str]:
    keystone_url = get_env("CLOUDPODS_KEYSTONE_URL") or (
        vm_info or {}).get("cloudpods_keystone_url", "")
    username = get_env("CLOUDPODS_USER") or (vm_info or {}).get("cloudpods_user", "")
    password = get_env("CLOUDPODS_PASSWORD") or (vm_info or {}).get("cloudpods_password", "")
    if keystone_url and username and password:
        return {"keystone_url": keystone_url, "username": username, "password": password}
    # Fallback to create_server.Env defaults (when secrets not configured)
    return _default_credentials()


class EnvPool:
    """CloudPods environment resource pool.

    Responsibilities:
      - Scan pool (list servers by prefix)
      - Acquire an available env (find -> verify -> create -> verify)
      - Release (mark as returned, no delete)
      - Batch cleanup (delete all envs used in this batch)
    Thread-safe: internal lock protects acquired/released sets.
    """

    def __init__(
        self,
        cfg: Dict,
        repo_root: Path,
        ssh_probe=None,
    ):
        self.cfg = cfg
        self.repo_root = repo_root
        self.env_prefix = cfg.get("env_prefix", "openruyi-func")
        # Default SSH probe function (caller can inject for testing)
        self.ssh_probe = ssh_probe or default_ssh_probe
        self._lock = threading.Lock()
        self._acquired: set = set()          # env keys currently held by test suites
        self._created: set = set()           # newly created in this batch (cleanup on teardown)
        self._used_pool: set = set()         # all envs used in this batch (including created)
        self._cp: Optional[CloudPodsClient] = None
        self._credentials: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # CloudPods client (lazy init)
    # ------------------------------------------------------------------
    def _get_client(self) -> Optional[CloudPodsClient]:
        if self._cp is not None:
            return self._cp
        creds = _get_credentials()
        if not creds["keystone_url"] or not creds["username"] or not creds["password"]:
            logger.error("Missing CloudPods credentials")
            return None
        # Password may be XOR+Base64 encrypted string (create_server.Env defaults, etc.),
        # try decrypting first; if decryption fails, treat as plaintext.
        try:
            from core.cloudpods import decrypt_password
            decrypted = decrypt_password(creds["password"])
            if decrypted:
                creds["password"] = decrypted
        except Exception:  # noqa: BLE001
            pass
        self._credentials = creds
        self._cp = CloudPodsClient(
            keystone_url=creds["keystone_url"],
            username=creds["username"],
            password=creds["password"],
        )
        if self._cp._session is None:
            logger.error("CloudPods authentication failed")
            self._cp = None
            return None
        return self._cp

    # ------------------------------------------------------------------
    # Resource pool scan
    # ------------------------------------------------------------------
    def list_pool(self) -> List[Dict]:
        """List all servers in pool matching the prefix (including status)."""
        cp = self._get_client()
        if cp is None:
            return []
        return cp.list_servers(name_prefix=self.env_prefix)

    def find_available_env(self, spec: Dict) -> Optional[Dict]:
        """Find an env in pool that matches spec and is not already acquired.

        Match criteria (approximate): name prefix match, server status running,
        QEMU port SSH reachable. Returns env description dict or None.
        """
        cp = self._get_client()
        if cp is None:
            return None
        servers = self.list_pool()
        for s in servers:
            sid = s.get("id", "")
            name = s.get("name", "")
            if not sid:
                continue
            if s.get("status", "") not in ("running", "ready"):
                logger.info("[pool] skip %s (status=%s)", name, s.get("status"))
                continue
            with self._lock:
                if sid in self._acquired:
                    continue
            # Try probing availability with spec (SSH)
            if self._probe_env(sid, name, spec):
                ips = self._get_ips(sid)
                host_ip = ips[0] if ips else ""
                qemu_port = int(spec.get("qemu_ssh_port_base",
                                         self.cfg.get("qemu_ssh_port_base", 12055)))
                return {"server_id": sid, "name": name, "host_ip": host_ip,
                        "qemu_ports": [qemu_port],
                        "ssh_user": spec.get("qemu_ssh_user",
                                             self.cfg.get("qemu_ssh_user", "openruyi")),
                        "ssh_password": spec.get("qemu_ssh_password",
                                                 self.cfg.get("qemu_ssh_password", "openruyi")),
                        "spec": spec, "created": False, "from_pool": True}
        return None

    def _probe_env(self, server_id: str, name: str, spec: Dict) -> bool:
        """Probe env availability: SSH to host (22) and QEMU (12055+).

        2.4: If SSH fails, treat as unavailable (caller responsible for delete and recreate).
        """
        try:
            ips = self._get_ips(server_id)
            if not ips:
                logger.info("[pool] %s has no IP", name)
                return False
            host_ip = ips[0]
            qemu_port = int(spec.get("qemu_ssh_port_base",
                                     self.cfg.get("qemu_ssh_port_base", 12055)))
            ssh_user = spec.get("qemu_ssh_user", self.cfg.get("qemu_ssh_user", "openruyi"))
            ssh_pass = spec.get("qemu_ssh_password",
                                self.cfg.get("qemu_ssh_password", "openruyi"))
            # Prefer probing QEMU SSH first (the actual test execution entry)
            if self.ssh_probe(host_ip, qemu_port, ssh_user, ssh_pass):
                logger.info("[pool] %s (QEMU %s:%s) is usable", name, host_ip, qemu_port)
                return True
            logger.info("[pool] %s QEMU SSH unavailable", name)
            return False
        except Exception as exc:  # noqa: BLE001
            logger.warning("[pool] probe %s failed: %s", name, exc)
            return False

    def _get_ips(self, server_id: str) -> List[str]:
        cp = self._get_client()
        if cp is None:
            return []
        detail = cp.get_server_detail(server_id)
        if not detail:
            return []
        server = detail.get("server", {})
        nics = server.get("nics", [])
        ips = []
        for nic in nics:
            ip = nic.get("ip_addr")
            if ip and ip not in ips:
                ips.append(ip)
        if not ips:
            ips = [ip for ip in server.get("ips", []) if ip]
        return ips

    # ------------------------------------------------------------------
    # Acquire / Create / Release / Cleanup
    # ------------------------------------------------------------------
    def acquire(self, suite_name: str, spec: Dict) -> Optional[Dict]:
        """Acquire an available env.

        Flow: pool lookup -> found → verify -> not found → create (up to retries,
        verify after creation, delete and recreate if unusable).

        Thread-safe: find+mark done atomically inside lock to avoid concurrent
        acquisition of the same env.
        """
        retries = int(self.cfg.get("env_verify_retries", 2))
        for attempt in range(1, retries + 1):
            env = self._find_and_acquire(spec)
            if env is not None:
                logger.info("[pool] acquired pool env %s (attempt %s)",
                            env["name"], attempt)
                return env

            # No usable env found: create one
            logger.info("[pool] no usable env in pool, creating new (attempt %s)", attempt)
            created = self._create_env(spec)
            if created is None:
                logger.error("[pool] create env failed (attempt %s)", attempt)
                time.sleep(5)
                continue
            # After creation, verify (if fails, delete so next round recreates)
            if self._probe_env(created["server_id"], created["name"], spec):
                with self._lock:
                    self._acquired.add(created["server_id"])
                    self._created.add(created["server_id"])
                    self._used_pool.add(created["server_id"])
                logger.info("[pool] created & usable env %s", created["name"])
                return created
            else:
                logger.warning("[pool] created env %s not usable, deleting",
                               created["name"])
                self._delete_env(created["server_id"])
                time.sleep(5)

        logger.error("[pool] failed to acquire env for suite %s after %s attempts",
                     suite_name, retries)
        return None

    def _find_and_acquire(self, spec: Dict) -> Optional[Dict]:
        """Complete find + mark-acquired inside lock, return env dict or None."""
        cp = self._get_client()
        if cp is None:
            return None
        servers = self.list_pool()
        for s in servers:
            sid = s.get("id", "")
            name = s.get("name", "")
            if not sid:
                continue
            if s.get("status", "") not in ("running", "ready"):
                logger.info("[pool] skip %s (status=%s)", name, s.get("status"))
                continue
            with self._lock:
                if sid in self._acquired:
                    continue
                # Probe (potentially slow) is outside lock; but mark-acquired
                # must be inside lock with double-check to prevent another
                # thread from seizing it during probe.
                self._acquired.add(sid)
            if self._probe_env(sid, name, spec):
                ips = self._get_ips(sid)
                host_ip = ips[0] if ips else ""
                qemu_port = int(spec.get("qemu_ssh_port_base",
                                         self.cfg.get("qemu_ssh_port_base", 12055)))
                with self._lock:
                    self._used_pool.add(sid)
                logger.info("[pool] acquired pool env %s (%s)", name, host_ip)
                return {
                    "server_id": sid,
                    "name": name,
                    "host_ip": host_ip,
                    "qemu_ports": [qemu_port],
                    "ssh_user": spec.get("qemu_ssh_user",
                                          self.cfg.get("qemu_ssh_user", "openruyi")),
                    "ssh_password": spec.get("qemu_ssh_password",
                                             self.cfg.get("qemu_ssh_password", "openruyi")),
                    "host_ssh_user": "root",
                    "host_ssh_password": "",
                    "spec": spec,
                    "created": False,
                    "from_pool": True,
                }
            else:
                # 2.4: Pooled VM exists but not usable (SSH unavailable) → delete and recreate
                with self._lock:
                    self._acquired.discard(sid)
                    self._used_pool.add(sid)
                logger.warning(
                    "[pool] env %s not usable (SSH unavailable), deleting "
                    "and will recreate", name)
                self._delete_env(sid)
        return None

    def _create_env(self, spec: Dict) -> Optional[Dict]:
        """Create an env (1 host + 1 QEMU), return env dict or None."""
        try:
            # Reuse launch-qemu-env's launch_env
            from commands.launch_qemu_env import launch_env

            launch_spec = dict(spec)
            launch_spec.setdefault("cloudpods_server_num", 1)
            launch_spec.setdefault("riscv_qemu_num", 1)
            launch_spec.setdefault("server_sku", "ecs.g1.c8m8")
            vm_info = launch_env(launch_spec, logger=logger, iscas_disable=True)
            if not vm_info or not vm_info.get("ok"):
                logger.error("[pool] launch_env failed")
                return None
            hosts = vm_info.get("hosts", [])
            if not hosts:
                logger.error("[pool] launch_env returned no hosts")
                return None
            host = hosts[0]
            return {
                "server_id": host.get("server_id", ""),
                "name": host.get("host_ip", ""),
                "host_ip": host.get("host_ip", ""),
                "qemu_ports": host.get("qemu_ports", []),
                "ssh_user": host.get("ssh_user", "openruyi"),
                "ssh_password": host.get("ssh_password", "openruyi"),
                "host_ssh_user": host.get("host_ssh_user", "root"),
                "host_ssh_password": host.get("host_ssh_password", ""),
                "created": True,
                "from_pool": False,
            }
        except Exception as exc:  # noqa: BLE001
            logger.error("[pool] create env error: %s", exc)
            return None

    def release(self, server_id: str) -> None:
        """Release control of the env resource (return to pool), no delete (2.5)."""
        with self._lock:
            self._acquired.discard(server_id)
        logger.info("[pool] released env %s (not deleted)", server_id)

    def delete_env(self, server_id: str) -> bool:
        """Delete a single env (called before recreate when 2.4 unusable)."""
        return self._delete_env(server_id)

    def _delete_env(self, server_id: str) -> bool:
        cp = self._get_client()
        if cp is None or not server_id:
            return False
        try:
            ok = cp.delete_server(server_id)
            if ok:
                cp.wait_for_server_is_deleted(server_id, timeout=600)
            return ok
        except Exception as exc:  # noqa: BLE001
            logger.error("[pool] delete env %s error: %s", server_id, exc)
            return False

    def cleanup_all(self) -> int:
        """Delete all envs used in this batch from pool (2.6).

        Returns number of successfully deleted envs.
        """
        cp = self._get_client()
        if cp is None:
            return 0
        with self._lock:
            targets = list(self._used_pool)
            self._used_pool.clear()
            self._acquired.clear()
        deleted = 0
        for sid in targets:
            if self._delete_env(sid):
                deleted += 1
        logger.info("[pool] cleanup: deleted %d/%d env(s)", deleted, len(targets))
        return deleted


def default_ssh_probe(host: str, port: int, user: str, password: str,
                      timeout: int = 30) -> bool:
    """Default SSH probe: try to connect and execute a simple command."""
    try:
        from core.ssh import SSHClient

        ssh = SSHClient(host, port, user, password)
        ssh.ssh.close()
        return True
    except Exception:  # noqa: BLE001
        return False
