# -*- coding: utf-8 -*-
"""资源池管理：CloudPods 环境的申请 / 校验 / 释放 / 清理。

需求 2.3~2.6 的实现：
  - 2.3 执行每个测试套前，根据所需条件，从 CloudPods 资源池中查找是否存在
        符合条件的虚拟机环境（名称前缀匹配 + SSH 可用性检查）；没有则创建一套。
  - 2.4 池中有虚拟机但不可用（无法 SSH）时，删除后重新创建一套。
  - 2.5 测试套执行完成后释放对该环境的控制（归还池），但不删除。
  - 2.6 所有测试套执行完成后，统一删除资源池中所有本次使用的环境。

环境定义：一个 CloudPods server（KVM host）+ 其上启动的 N 个 QEMU VM。
资源池按名称前缀区分（env_prefix），一套环境 = 一个 server。
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

# CloudPods 凭据：环境变量优先 -> 显式传入 -> create_server.Env 默认值
def _default_credentials() -> Dict[str, str]:
    """读取 create_server.Env 的默认凭据（与 launch_env 创建时保持一致）。"""
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
    # 回退到 create_server.Env 默认凭据（如 secrets 未配置时）
    return _default_credentials()


class EnvPool:
    """CloudPods 环境资源池。

    负责：
      - 扫描资源池（按前缀列出 server）
      - 申请一套可用环境（find -> verify -> create -> verify）
      - 释放（标记归还，不删除）
      - 统一清理（删除池中所有本批次环境）
    线程安全：内部用锁保护已分配/已释放集合。
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
        # 默认 SSH 探测函数（可由调用方注入便于测试）
        self.ssh_probe = ssh_probe or default_ssh_probe
        self._lock = threading.Lock()
        self._acquired: set = set()          # 当前被测试套占用的 env key
        self._created: set = set()           # 本批次新创建（统一清理时删除）
        self._used_pool: set = set()         # 本批次使用过的池内环境（含创建）
        self._cp: Optional[CloudPodsClient] = None
        self._credentials: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # CloudPods 客户端（懒加载）
    # ------------------------------------------------------------------
    def _get_client(self) -> Optional[CloudPodsClient]:
        if self._cp is not None:
            return self._cp
        creds = _get_credentials()
        if not creds["keystone_url"] or not creds["username"] or not creds["password"]:
            logger.error("Missing CloudPods credentials")
            return None
        # 密码可能是 XOR+Base64 加密串（create_server.Env 默认值等），
        # 先尝试解密；解密失败则视为明文原样使用。
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
    # 资源池扫描
    # ------------------------------------------------------------------
    def list_pool(self) -> List[Dict]:
        """列出资源池中所有符合前缀的 server（含状态）。"""
        cp = self._get_client()
        if cp is None:
            return []
        return cp.list_servers(name_prefix=self.env_prefix)

    def find_available_env(self, spec: Dict) -> Optional[Dict]:
        """在资源池中查找一套满足 spec 且未被占用的环境。

        匹配条件（近似）：名称前缀匹配、server 状态 running、
        QEMU 端口 SSH 可达。返回 env 描述 dict 或 None。
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
            # 尝试用 spec 探测可用性（SSH）
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
        """探测环境是否可用：SSH 到 host（22）和 QEMU（12055+）。

        2.4：无法 SSH 则视为不可用（调用方负责删除重建）。
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
            # 优先探测 QEMU SSH（真正执行测试的入口）
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
    # 申请 / 创建 / 释放 / 清理
    # ------------------------------------------------------------------
    def acquire(self, suite_name: str, spec: Dict) -> Optional[Dict]:
        """申请一套可用环境。

        流程：资源池查找 -> 找到则验证 -> 未找到则创建（最多 retries 次，
        创建后验证，不可用则删除重建）。

        线程安全：find+标记在锁内原子完成，避免并发抢占同一环境。
        """
        retries = int(self.cfg.get("env_verify_retries", 2))
        for attempt in range(1, retries + 1):
            env = self._find_and_acquire(spec)
            if env is not None:
                logger.info("[pool] acquired pool env %s (attempt %s)",
                            env["name"], attempt)
                return env

            # 未找到可用环境：创建一套
            logger.info("[pool] no usable env in pool, creating new (attempt %s)", attempt)
            created = self._create_env(spec)
            if created is None:
                logger.error("[pool] create env failed (attempt %s)", attempt)
                time.sleep(5)
                continue
            # 创建成功后验证（若失败，删除后下一轮重建）
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
        """在锁内完成「查找 + 标记占用」，返回 env dict 或 None。"""
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
                # 探测（可能耗时）不在锁内；但标记占用要在锁内且需
                # 二次确认，避免探测期间被其他线程抢先。
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
                # 2.4：池中有虚拟机但不可用（无法 SSH）→ 删除后重建
                with self._lock:
                    self._acquired.discard(sid)
                    self._used_pool.add(sid)
                logger.warning(
                    "[pool] env %s not usable (SSH unavailable), deleting "
                    "and will recreate", name)
                self._delete_env(sid)
        return None

    def _create_env(self, spec: Dict) -> Optional[Dict]:
        """创建一套环境（1 host + 1 QEMU），返回 env dict 或 None。"""
        try:
            # 复用 launch-qemu-env 的 launch_env
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
        """释放对环境资源的控制（归还池），但不删除（2.5）。"""
        with self._lock:
            self._acquired.discard(server_id)
        logger.info("[pool] released env %s (not deleted)", server_id)

    def delete_env(self, server_id: str) -> bool:
        """删除单个环境（2.4 不可用时重建前调用）。"""
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
        """统一删除资源池中本批次使用过的所有环境（2.6）。

        返回删除成功的数量。
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
    """默认 SSH 探测：尝试建立连接并执行简单命令。"""
    try:
        from core.ssh import SSHClient

        ssh = SSHClient(host, port, user, password)
        ssh.ssh.close()
        return True
    except Exception:  # noqa: BLE001
        return False
