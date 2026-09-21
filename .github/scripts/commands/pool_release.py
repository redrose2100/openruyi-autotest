# -*- coding: utf-8 -*-
"""pool-release command: release pool environment (delete CloudPods VM and rebuild to ensure no leftovers)."""
from __future__ import annotations

import json
import logging

from core.base import BaseCommand
from pool.core import get_pool

logger = logging.getLogger("ci_cli.commands.pool_release")


class PoolReleaseCommand(BaseCommand):
    """Release pool environment: delete CloudPods VM and rebuild a new one into the pool"""

    name = "pool-release"
    description = "Release CI pre-provisioned pool environment (delete old, build new, ensure no CloudPods leftovers)"

    def setup_parser(self, parser):
        parser.add_argument("--server-id", default="",
                            help="CloudPods server ID to release")
        parser.add_argument("--qemu-num", type=int, default=1,
                            help="QEMU count (1→Pool A, 2→Pool B), default 1")
        parser.add_argument("--pool-info", default="",
                            help="JSON file generated during pool acquire (contains server_id)")

    def run(self, args) -> int:
        server_id = args.server_id
        qemu_num = args.qemu_num

        # Support reading from pool_info / vm_info file
        if args.pool_info:
            try:
                with open(args.pool_info, "r", encoding="utf-8") as f:
                    info = json.load(f)
                # vm_info format: _pool sub-object
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
        self.log_info("Released %s back to pool (VM kept for reuse)", server_id[:12])
        return 0