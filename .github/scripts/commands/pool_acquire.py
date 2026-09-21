# -*- coding: utf-8 -*-
"""pool-acquire command: acquire an environment from the pre-provisioned pool."""
from __future__ import annotations

import json
import logging

from core.base import BaseCommand
from pool.core import get_pool

logger = logging.getLogger("ci_cli.commands.pool_acquire")


class PoolAcquireCommand(BaseCommand):
    """Acquire an environment from the CI pre-provisioned pool (blocking until success or timeout)"""

    name = "pool-acquire"
    description = "Acquire a QEMU environment from the CI pre-provisioned pool"

    def setup_parser(self, parser):
        parser.add_argument("--requirements", default="vm_requirements.json",
                            help="Path to vm_requirements.json (contains server_count)")
        parser.add_argument("--server-count", type=int, default=0,
                            help="Directly specify QEMU count (1→pool A, 2→pool B), 0=read from requirements")
        parser.add_argument("--timeout", type=int, default=600,
                            help="Max wait seconds, default 600")
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

        # Wrap into vm_info compatible format
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
            # Pool metadata (for release use)
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