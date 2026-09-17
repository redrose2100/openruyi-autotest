# -*- coding: utf-8 -*-
"""pool-release 命令：释放池环境（删除 CloudPods VM 并重建，确保无残留）。"""
from __future__ import annotations

import json
import logging

from core.base import BaseCommand
from pool.core import get_pool

logger = logging.getLogger("ci_cli.commands.pool_release")


class PoolReleaseCommand(BaseCommand):
    """释放池环境：删除 CloudPods VM 并重建一台新 VM 放回池中"""

    name = "pool-release"
    description = "释放 CI 预置池环境（删旧建新，确保 CloudPods 无残留）"

    def setup_parser(self, parser):
        parser.add_argument("--server-id", default="",
                            help="待释放的 CloudPods server ID")
        parser.add_argument("--qemu-num", type=int, default=1,
                            help="QEMU 数量（1→池A, 2→池B），默认 1")
        parser.add_argument("--pool-info", default="",
                            help="pool acquire 时生成的 JSON 文件（含 server_id）")

    def run(self, args) -> int:
        server_id = args.server_id
        qemu_num = args.qemu_num

        # 支持从 pool_info / vm_info 文件读取
        if args.pool_info:
            try:
                with open(args.pool_info, "r", encoding="utf-8") as f:
                    info = json.load(f)
                # vm_info 格式：_pool 子对象
                pm = info.get("_pool", {})
                if not server_id:
                    server_id = pm.get("server_id", info.get("server_id", ""))
                if args.qemu_num == 1:
                    qemu_num = pm.get("qemu_num", qemu_num)
            except (FileNotFoundError, json.JSONDecodeError):
                self.log_error("Failed to read pool-info: %s", args.pool_info)
                return 1

        if not server_id:
            self.log_error("No server_id provided")
            return 1

        pool = get_pool(qemu_num)
        if pool is None:
            self.log_error("Unknown pool for qemu_num=%d", qemu_num)
            return 1

        result = pool.release(server_id)
        if result:
            self.log_info("Released & recreated %s", result["server_id"][:12])
        else:
            self.log_warn("VM deleted but rebuild failed for %s", server_id[:12])
        return 0