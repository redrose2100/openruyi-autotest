# -*- coding: utf-8 -*-
"""
CloudPods API client (shared library).

Design highlights:
  * Extracted from tools/cloudpods/create_server.py's CloudPodsClient for reuse across
    multiple commands (launch-qemu-env create/wait, cleanup-cloudpods delete), avoiding
    duplicate implementations.
  * Maintains full method signature compatibility with the original CloudPodsClient
    (the same-named class in create_server.py remains the canonical implementation;
    this is a command-oriented lightweight wrapper + credential decryption utility).
"""
from __future__ import annotations

import hashlib
import logging
import re
import time
from typing import Dict, List, Optional

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("ci_cli.cloudpods")

_MASTER_KEY = "openruyi-autotest-2024-secret-key"


def derive_key(master_key: str) -> bytes:
    """Derive a 32-byte key from master key using SHA-256."""
    return hashlib.sha256(master_key.encode()).digest()


def decrypt_password(encrypted: str, master_key: str = _MASTER_KEY) -> str:
    """Decrypt XOR+Base64 encrypted password."""
    key = derive_key(master_key)
    encrypted_bytes = __import__("base64").b64decode(encrypted)
    decrypted = bytes(
        [encrypted_bytes[i] ^ key[i % len(key)] for i in range(len(encrypted_bytes))]
    )
    return decrypted.decode("utf-8")


class CloudPodsClient:
    """CloudPods REST API client (lightweight, for CI command usage)."""

    def __init__(
        self,
        keystone_url: str,
        username: str,
        password: str,
        domain: str = "default",
        project: str = "system",
    ):
        self._keystone_url = keystone_url
        self._username = username
        self._password = password
        self._domain = domain
        self._project = project
        self._session = self._get_session()
        self._endpoints = self._get_endpoint()
        self._compute_url = f"{self._endpoints.get('region2', '')}/"

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------
    def _get_session(self) -> Optional[requests.Session]:
        session = requests.Session()
        session.headers["User-Agent"] = "yunioncloud-go/201708"
        url = f"{self._keystone_url}/auth/tokens"
        data = {
            "auth": {
                "context": {"source": "cli"},
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {"name": self._username, "password": self._password}
                    },
                },
                "scope": {
                    "project": {"domain": {"name": self._domain}, "name": self._project}
                },
            }
        }
        try:
            rs = session.post(url=url, json=data, verify=False, timeout=600)
            if rs.status_code != 200:
                logger.error("Keystone auth failed: status=%s", rs.status_code)
                return None
            token = rs.headers.get("X-Subject-Token", "")
            if not token:
                logger.error("Keystone auth failed: no token")
                return None
            session.headers["X-Auth-Token"] = token
            logger.info("CloudPods session created, token=%s...", token[:20])
            return session
        except Exception as e:  # noqa: BLE001
            logger.error("Keystone auth error: %s", e)
            return None

    def _get_endpoint(self) -> Dict[str, str]:
        try:
            url = f"{self._keystone_url}/endpoints"
            rs = self._session.get(url=url, verify=False, timeout=600)
            if rs.status_code != 200:
                return {}
            data = rs.json()
            endpoints: Dict[str, str] = {}
            for ep in data.get("endpoints", []):
                name = ep.get("service_name", "")
                ep_url = ep.get("url", "")
                if name and ep_url:
                    # Prefer IP-form endpoint (cross-platform compatible)
                    if name in endpoints:
                        existing = endpoints[name]
                        if not re.match(r"https?://\d+\.\d+\.\d+\.\d+", existing) and re.match(
                            r"https?://\d+\.\d+\.\d+\.\d+", ep_url
                        ):
                            endpoints[name] = ep_url
                    else:
                        endpoints[name] = ep_url
            return endpoints
        except Exception:  # noqa: BLE001
            return {}

    def _request(self, method: str, path: str, **kwargs) -> Optional[requests.Response]:
        url = f"{self._compute_url}{path.lstrip('/')}"
        try:
            kwargs.setdefault("verify", False)
            kwargs.setdefault("timeout", 600)
            return self._session.request(method, url, **kwargs)
        except Exception as e:  # noqa: BLE001
            logger.error("Request %s %s failed: %s", method, url, e)
            return None

    # ------------------------------------------------------------------
    # Server lifecycle
    # ------------------------------------------------------------------
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
        """Create one or more KVM VMs, return list of server_id."""
        if disks is None:
            disks = []
        if nets_list is None:
            nets_list = []
        nets = [{"network": net} for net in nets_list]

        server_config: Dict = {
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

        logger.info("Creating %s server(s), name=%s, sku=%s, arch=%s",
                    count, vm_name, sku, arch)
        rs = self._request("POST", "/servers", json={"count": count, "server": server_config})
        if rs is None or rs.status_code != 200:
            logger.error("Create server failed: status=%s",
                         rs.status_code if rs else "None")
            return []

        result = rs.json()
        server_ids: List[str] = []
        if "server" in result and "id" in result["server"]:
            server_ids.append(result["server"]["id"])
        elif "servers" in result:
            for s in result["servers"]:
                sid = s.get("body", {}).get("id", "")
                if sid:
                    server_ids.append(sid)
        logger.info("Created servers: %s", server_ids)
        return server_ids

    def get_server_detail(self, server_id: str) -> Optional[Dict]:
        rs = self._request("GET", f"/servers/{server_id}")
        if rs and rs.status_code == 200:
            return rs.json()
        return None

    def list_servers(self, name_prefix: str = "", limit: int = 0) -> List[Dict]:
        """List CloudPods servers by name prefix (abbreviated fields).

        The CloudPods API name parameter does exact match, while server names are
        formatted as ``{prefix}-{uuid_suffix}`` (generate_name mechanism), so the API
        cannot filter by prefix directly. Fetch all servers then filter by prefix client-side.

        Returns a list, each item containing id / name / status / ips and other key fields;
        returns empty list on query failure.
        """
        params: Dict = {"scope": "system", "details": "false"}
        if limit:
            params["limit"] = limit
        # Don't pass name param: CloudPods API name is exact match, but server naming format
        # is openruyi-ci-pool-1q-xxxxxxxx, which won't match a prefix. Filter client-side instead.
        rs = self._request("GET", "/servers", params=params)
        if rs is None or rs.status_code != 200:
            logger.error("List servers failed: status=%s",
                         rs.status_code if rs else "None")
            return []
        data = rs.json()
        servers = data.get("servers", [])
        result: List[Dict] = []
        for s in servers:
            name = s.get("name", "")
            if name_prefix and not name.startswith(name_prefix):
                continue
            result.append({
                "id": s.get("id", ""),
                "name": name,
                "status": s.get("status", ""),
                "ips": s.get("ips", []),
            })
        logger.info("List servers(name_prefix=%r) -> %d server(s)",
                    name_prefix, len(result))
        return result

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
        """Wait for the server to enter running status."""
        logger.info("Waiting for server %s to be running (timeout=%ss)...",
                    server_id, timeout)
        start = time.time()
        running_count = 0
        while True:
            if time.time() - start > timeout:
                logger.error("Timeout waiting for server %s", server_id)
                return False
            detail = self.get_server_detail(server_id)
            if not detail:
                time.sleep(5)
                continue
            status = detail.get("server", {}).get("status", "")
            if "_fail" in status or status in ("disk_fail", "deploy_fail", "ready"):
                logger.error("Server %s in bad status: %s", server_id, status)
                return False
            if status == "running":
                running_count += 1
                if running_count > 5:
                    logger.info("Server %s is running (confirmed %s times)",
                                server_id, running_count)
                    return True
                time.sleep(1)
            else:
                running_count = 0
                logger.info("Server %s status=%s, waiting...", server_id, status)
                time.sleep(5)

    def delete_server(self, server_id: str) -> bool:
        rs = self._request("DELETE", f"/servers/{server_id}")
        if rs and rs.status_code == 200:
            logger.info("Deleted server %s", server_id)
            return True
        logger.error("Failed to delete server %s (status=%s)",
                     server_id, rs.status_code if rs else "None")
        return False

    def wait_for_server_is_deleted(self, server_id: str, timeout: int = 600) -> bool:
        logger.info("Waiting for server %s to be deleted...", server_id)
        start = time.time()
        while time.time() - start < timeout:
            detail = self.get_server_detail(server_id)
            if not detail:
                logger.info("Server %s deleted", server_id)
                return True
            time.sleep(5)
        return False
