# -*- coding: utf-8 -*-
"""pool-acquire 命令：从预置池中申请一套环境。"""
from __future__ import annotations

import json
import logging

from core.base import BaseCommand
from pool.core import get_pool

logger = logging.getLogger("ci_cli.commands.pool_acquire")


class PoolAcquireCommand(BaseCommand):
    """从 CI 预置池申请环境（阻塞等待直到成功或超时）"""

    name = "pool-acquire"
    description = "从 CI 预置池中申请一套 QEMU 环境"

    def setup_parser(self, parser):
        parser.add_argument("--requirements", default="vm_requirements.json",
                            help="Path to vm_requirements.json（含 server_count）")
        parser.add_argument("--server-count", type=int, default=0,
                            help="直接指定 QEMU 数量（1→池A, 2→池B），0=从 requirements 读取")
        parser.add_argument("--timeout", type=int, default=600,
                            help="最大等待秒数，默认 600")
        parser.add_argument("--output", default="pool_env.json",
                            help="Output pool env JSON path")

    def run(self, args) -> int:
        server_count = args.server_count
        if server_count <= 0:
            try:
                with open(args.requirements, encoding="utf-8") as f:
                    req = json.load(f)
                server_count = req.get("server_count", 1)
            except (FileNotFoundError, json.JSONDecodeError):
                self.log_error("Cannot read server_count from %s", args.requirements)
                return 1

        pool = get_pool(server_count)
        if pool is None:
            self.log_error("No pool for server_count=%d", server_count)
            return 1

        self.log_info("Acquiring from pool (%d QEMU, timeout %ds)...",
                      server_count, args.timeout)
        env = pool.acquire(timeout=args.timeout)
        if env is None:
            self.log_error("Pool acquire failed/timeout")
            return 1

        # 包装为 vm_info 兼容格式
        vm_info = {
            "ok": True,
            "hosts": [{
                "host_ip": env["host_ip"],
                "qemu_ports": env["qemu_ports"],
                "ssh_user": env["ssh_user"],
                "ssh_password": env["ssh_password"],
                "host_ssh_user": env.get("host_ssh_user", "root"),
                "host_ssh_password": env.get("host_ssh_password", ""),
            }],
            # 池化元信息（供 release 使用）
            "_pool": {
                "server_id": env["server_id"],
                "qemu_num": server_count,
            },
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(vm_info, f, ensure_ascii=False, indent=2)
        self.log_info("Pool acquired: %s (%s:%s)",
                      env["server_id"][:12], env["host_ip"], env["qemu_ports"])
        return 0