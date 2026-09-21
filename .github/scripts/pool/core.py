# -*- coding: utf-8 -*-
"""Persistent CI pre-provisioned environment pool (dual-pool architecture).

Pool A: 1 QEMU/VM, max 20 (default single-server scenario)
Pool B: 2 QEMU/VM, max 5, SKU c16m16 (dual-server scenario)

Lifecycle:
  - Persistent: preserved across CI runs; provision is idempotent
  - Task arrives → determine pool by server count → check then create → release on completion (delete old VM + rebuild new VM back to pool)
  - Self-healing: probe fails → delete and rebuild
  - Image change (riscv64 URL hash change) → full pool rebuild
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from core.cloudpods import CloudPodsClient, decrypt_password
from core.config import get_env

logger = logging.getLogger("ci_cli.pool")

# ── Pool A config ──
POOL_A_PREFIX = "openruyi-ci-pool-1q"
POOL_A_MAX = 20
POOL_A_SKU = "ecs.g1.c8m8"
POOL_A_QEMU_NUM = 1

# ── Pool B config ──
POOL_B_PREFIX = "openruyi-ci-pool-2q"
POOL_B_MAX = 5
POOL_B_SKU = "ecs.g1.c16m16"
POOL_B_QEMU_NUM = 2

# ── Credentials ──
def _get_credentials() -> Dict[str, str]:
    keystone_url = get_env("CLOUDPODS_KEYSTONE_URL")
    username = get_env("CLOUDPODS_USER")
    password = get_env("CLOUDPODS_PASSWORD")
    if keystone_url and username and password:
        return {"keystone_url": keystone_url, "username": username, "password": password}
    try:
        from cloudpods import create_server as cs
        return {
            "keystone_url": getattr(cs.Env, "cloudpods_keystone_url", ""),
            "username": getattr(cs.Env, "cloudpods_user", ""),
            "password": getattr(cs.Env, "cloudpods_password", ""),
        }
    except Exception:
        return {"keystone_url": "", "username": "", "password": ""}


# ── Image version ──
def _get_image_url() -> str:
    """Read riscv64 image URL from create_server.Env."""
    try:
        from cloudpods import create_server as cs
        return getattr(cs.Env, "riscv_image_url", "")
    except Exception:
        return ""


def _compute_image_hash(image_url: str, work_dir: str = "/tmp") -> str:
    """Download image and compute sha256 (persistent image version identifier)."""
    import os
    import tempfile
    import subprocess
    if not image_url:
        return ""
    cache_file = os.path.join(work_dir, ".ci_pool_image.sha256")
    # If cache file exists and is less than 24h old, read directly
    if os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        if time.time() - mtime < 86400:
            with open(cache_file, "r") as f:
                return f.read().strip()
    # Download + compute
    logger.info("[pool] computing image hash for %s ...", image_url)
    fd, tmp = tempfile.mkstemp(suffix=".qcow2.xz")
    os.close(fd)
    try:
        subprocess.run(
            ["wget", "-q", "-O", tmp, image_url],
            timeout=3600, check=True, capture_output=True,
        )
        sha = hashlib.sha256()
        with open(tmp, "rb") as f:
            while True:
                chunk = f.read(8 * 1024 * 1024)
                if not chunk:
                    break
                sha.update(chunk)
        h = sha.hexdigest()
        with open(cache_file, "w") as f:
            f.write(h)
        logger.info("[pool] image hash: %s", h[:16])
        return h
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


# ── Pool entries ──
POOL_META_FILE = "/tmp/.ci_pool_meta.json"
_pool_lock = threading.Lock()


def _pool_meta_path() -> str:
    return POOL_META_FILE


def _load_meta() -> Dict[str, Any]:
    try:
        with open(_pool_meta_path(), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_meta(meta: Dict[str, Any]) -> None:
    with open(_pool_meta_path(), "w") as f:
        json.dump(meta, f, indent=2)


# ── CloudPods client (lazy) ──
_cp_cache: Optional[CloudPodsClient] = None


def _get_cp() -> Optional[CloudPodsClient]:
    global _cp_cache
    if _cp_cache is not None:
        return _cp_cache
    creds = _get_credentials()
    if not creds["keystone_url"] or not creds["username"] or not creds["password"]:
        logger.error("[pool] missing CloudPods credentials")
        return None
    pw = creds["password"]
    try:
        dpw = decrypt_password(pw)
        if dpw:
            pw = dpw
    except Exception:
        pass
    _cp_cache = CloudPodsClient(
        keystone_url=creds["keystone_url"],
        username=creds["username"],
        password=pw,
    )
    return _cp_cache


# ── SSH probe ──
def _ssh_probe(host: str, ports: List[int], user: str = "openruyi",
               password: str = "openruyi", timeout: int = 30) -> bool:
    """Probe QEMU SSH availability. All ports must be reachable."""
    try:
        from core.ssh import SSHClient
        for port in ports:
            logger.info("[debug] SSH probe: host=%s port=%s user=%s password=%s",
                        host, port, user, password)
            ssh = SSHClient(host, port, user, password, connect_timeout=timeout)
            ssh.close()
        logger.info("[debug] SSH probe SUCCESS: host=%s ports=%s", host, ports)
        return True
    except Exception as exc:
        logger.warning("[debug] SSH probe FAILED: host=%s ports=%s user=%s error=%s",
                       host, ports, user, exc)
        return False


# ── Create one env ──
def _create_env(qemu_num: int, sku: str, pool_prefix: str) -> Optional[Dict]:
    """Create one env: 1 host + qemu_num QEMU VMs. Returns env dict or None."""
    from commands.launch_qemu_env import launch_env
    from cloudpods import create_server as cs

    # Save original prefix and temporarily override
    orig_prefix = cs.Env.server_name_prefix
    cs.Env.server_name_prefix = pool_prefix

    spec = {
        "cloudpods_server_num": 1,
        "riscv_qemu_num": qemu_num,
        "riscv_qemu_cpu": 4 if qemu_num == 1 else 8,
        "riscv_qemu_memory": 4 if qemu_num == 1 else 8,
        "riscv_qemu_net_num": 1,
        "riscv_qemu_disks": "[]",
        "server_sku": sku,
    }
    try:
        vm_info = launch_env(spec, logger=logger, iscas_disable=True)
        if not vm_info or not vm_info.get("ok"):
            return None
        hosts = vm_info.get("hosts", [])
        if not hosts:
            return None
        h = hosts[0]
        return {
            "server_id": h.get("server_id", ""),
            "name": h.get("host_ip", ""),
            "host_ip": h.get("host_ip", ""),
            "qemu_ports": h.get("qemu_ports", []),
            "ssh_user": h.get("ssh_user", "openruyi"),
            "ssh_password": h.get("ssh_password", "openruyi"),
            "host_ssh_user": h.get("host_ssh_user", "root"),
            "host_ssh_password": h.get("host_ssh_password", ""),
        }
    finally:
        cs.Env.server_name_prefix = orig_prefix


def _delete_env(server_id: str) -> bool:
    cp = _get_cp()
    if cp is None or not server_id:
        return False
    try:
        ok = cp.delete_server(server_id)
        if ok:
            cp.wait_for_server_is_deleted(server_id, timeout=600)
        return ok
    except Exception:
        return False


# ── Pool scan ──
def _list_servers(prefix: str) -> List[Dict]:
    cp = _get_cp()
    if cp is None:
        return []
    return cp.list_servers(name_prefix=prefix)


def _get_server_ip(server_id: str) -> str:
    cp = _get_cp()
    if cp is None:
        return ""
    detail = cp.get_server_detail(server_id)
    if not detail:
        logger.warning("[debug] get_server_detail(%s) returned None/empty", server_id[:12])
        return ""
    server = detail.get("server", {})
    nics = server.get("nics", [])
    logger.info("[debug] server %s: nics=%s, ips=%s",
                server_id[:12], nics, server.get("ips", []))
    for nic in nics:
        ip = nic.get("ip_addr")
        if ip:
            return ip
    for ip in server.get("ips", []):
        if ip:
            return ip
    logger.warning("[debug] server %s: no IP found in nics or ips", server_id[:12])
    return ""


# ── Pool definition ──
class CIPool:
    """CI persistent pre-provisioned pool (single pool)."""

    def __init__(self, prefix: str, max_count: int, qemu_num: int, sku: str):
        self.prefix = prefix
        self.max_count = max_count
        self.qemu_num = qemu_num
        self.sku = sku
        self._acquired: Set[str] = set()
        self._lock = threading.Lock()

    # ── Query ──
    def list_all(self) -> List[Dict]:
        return _list_servers(self.prefix)

    def count(self) -> int:
        return len(self.list_all())

    # ── Acquire ──
    def acquire(self, timeout: int = 600) -> Optional[Dict]:
        """Acquire an available env from pool. Try to create if none available.
        Queue and wait until timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            env = self._find_and_acquire()
            if env:
                return env
            # None available → create
            if self.count() < self.max_count:
                created = _create_env(self.qemu_num, self.sku, self.prefix)
                if created:
                    sid = created["server_id"]
                    with self._lock:
                        self._acquired.add(sid)
                    logger.info("[pool:%s] created & acquired %s", self.prefix, sid[:12])
                    return created
                logger.warning("[pool:%s] create failed", self.prefix)
            logger.info("[pool:%s] pool full (%d/%d), waiting ...",
                        self.prefix, self.count(), self.max_count)
            time.sleep(15)
        logger.error("[pool:%s] acquire timeout after %ds", self.prefix, timeout)
        return None

    def _find_and_acquire(self) -> Optional[Dict]:
        servers = self.list_all()
        qemu_ports = [12055 + i for i in range(self.qemu_num)]
        logger.info("[debug] pool:%s scanning %d server(s), qemu_ports=%s",
                    self.prefix, len(servers), qemu_ports)
        for s in servers:
            sid = s.get("id", "")
            sname = s.get("name", "")
            sstatus = s.get("status", "")
            logger.info("[debug] pool:%s check server id=%s name=%s status=%s",
                        self.prefix, sid[:12] if sid else "N/A", sname, sstatus)
            if not sid or sstatus not in ("running", "ready"):
                logger.info("[debug] pool:%s skip %s (bad status: %s)", self.prefix, sid[:12] if sid else "N/A", sstatus)
                continue
            with self._lock:
                if sid in self._acquired:
                    logger.info("[debug] pool:%s skip %s (already acquired)", self.prefix, sid[:12])
                    continue
            host_ip = _get_server_ip(sid)
            if not host_ip:
                logger.info("[debug] pool:%s skip %s (no host_ip)", self.prefix, sid[:12])
                continue
            if _ssh_probe(host_ip, qemu_ports):
                with self._lock:
                    if sid in self._acquired:
                        continue
                    self._acquired.add(sid)
                logger.info("[pool:%s] acquired %s (%s)", self.prefix, s.get("name", ""), host_ip)
                return {
                    "server_id": sid,
                    "name": s.get("name", ""),
                    "host_ip": host_ip,
                    "qemu_ports": qemu_ports,
                    "ssh_user": "openruyi",
                    "ssh_password": "openruyi",
                    "host_ssh_user": "root",
                    "host_ssh_password": "ISRCpassword@123",
                }
            else:
                # probe failed → delete and rebuild
                logger.warning("[pool:%s] %s probe failed, deleting", self.prefix, sid[:12])
                _delete_env(sid)
        return None

    # ── Release ──
    def release(self, server_id: str) -> Optional[Dict]:
        """Release env back to pool: only remove from acquired set, do not delete VM.

        VM stays in CloudPods for reuse by next acquire; _find_and_acquire()
        has SSH probe health check, unhealthy VMs are auto-deleted and rebuilt
        during scan.

        Returns:
            server_id (always returns non-None indicating release success).
        """
        with self._lock:
            self._acquired.discard(server_id)
        logger.info("[pool:%s] released %s (VM kept, will be reused)", self.prefix, server_id[:12])
        return {"server_id": server_id}

    # ── Image version check ──
    def image_version(self, work_dir: str = "/tmp") -> str:
        return _compute_image_hash(_get_image_url(), work_dir)

    # ── Cleanup ──
    def delete_all(self) -> int:
        servers = self.list_all()
        deleted = 0
        for s in servers:
            sid = s.get("id", "")
            if sid and _delete_env(sid):
                deleted += 1
        with self._lock:
            self._acquired.clear()
        logger.info("[pool:%s] deleted %d servers", self.prefix, deleted)
        return deleted

    # ── Health check ──
    def probe_all(self) -> List[Dict]:
        """Scan health status of all servers in pool."""
        result = []
        servers = self.list_all()
        qemu_ports = [12055 + i for i in range(self.qemu_num)]
        for s in servers:
            sid = s.get("id", "")
            name = s.get("name", "")
            host_ip = _get_server_ip(sid)
            healthy = _ssh_probe(host_ip, qemu_ports) if host_ip else False
            result.append({
                "server_id": sid, "name": name, "host_ip": host_ip,
                "status": s.get("status", ""), "healthy": healthy,
                "qemu_ports": qemu_ports,
            })
        return result


# ── Dual-pool management ──
def _build_pools() -> Dict[str, CIPool]:
    return {
        "1q": CIPool(POOL_A_PREFIX, POOL_A_MAX, POOL_A_QEMU_NUM, POOL_A_SKU),
        "2q": CIPool(POOL_B_PREFIX, POOL_B_MAX, POOL_B_QEMU_NUM, POOL_B_SKU),
    }


def get_pool(qemu_num: int) -> Optional[CIPool]:
    """Return the corresponding pool based on required QEMU count. 1 → Pool A, 2 → Pool B."""
    pools = _build_pools()
    if qemu_num == 1:
        return pools["1q"]
    if qemu_num == 2:
        return pools["2q"]
    return None