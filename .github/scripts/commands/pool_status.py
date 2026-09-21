# -*- coding: utf-8 -*-
"""pool-status command: view dual-pool status and health info."""
from __future__ import annotations

import json
import logging

from core.base import BaseCommand
from pool.core import (
    POOL_A_PREFIX, POOL_A_MAX, POOL_A_QEMU_NUM,
    POOL_B_PREFIX, POOL_B_MAX, POOL_B_QEMU_NUM,
    _list_servers, _get_server_ip, _ssh_probe, _compute_image_hash, _get_image_url,
)

logger = logging.getLogger("ci_cli.commands.pool_status")


class PoolStatusCommand(BaseCommand):
    """List all VMs and health status in both pools"""

    name = "pool-status"
    description = "List CI pre-provisioned env pool status and health info"

    def setup_parser(self, parser):
        parser.add_argument("--output", default="",
                            help="Output JSON path")
        parser.add_argument("--image-work-dir", default="/tmp",
                            help="Image hash cache directory")

    def run(self, args) -> int:
        image_url = _get_image_url()
        image_hash = _compute_image_hash(image_url, args.image_work_dir) if image_url else ""

        pool_a = self._scan("A", POOL_A_PREFIX, POOL_A_MAX, POOL_A_QEMU_NUM)
        pool_b = self._scan("B", POOL_B_PREFIX, POOL_B_MAX, POOL_B_QEMU_NUM)

        total_healthy = sum(1 for s in pool_a if s["healthy"]) + sum(1 for s in pool_b if s["healthy"])
        total_count = len(pool_a) + len(pool_b)
        self.log_info("=" * 60)
        self.log_info("CI Pool Status  |  Image: %s", (image_hash or "N/A")[:16])
        self.log_info("-" * 60)
        self._print_pool("Pool A (1 QEMU)", pool_a, POOL_A_MAX)
        self._print_pool("Pool B (2 QEMU)", pool_b, POOL_B_MAX)
        self.log_info("-" * 60)
        self.log_info("Total: %d/%d healthy", total_healthy, total_count)

        if args.output:
            result = {
                "image_hash": image_hash,
                "pool_a": pool_a,
                "pool_b": pool_b,
            }
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        return 0

    def _scan(self, label: str, prefix: str, _max: int, qemu_num: int) -> list:
        servers = _list_servers(prefix)
        qemu_ports = [12055 + i for i in range(qemu_num)]
        result = []
        for s in servers:
            sid = s.get("id", "")
            host_ip = _get_server_ip(sid)
            healthy = _ssh_probe(host_ip, qemu_ports) if host_ip else False
            result.append({
                "server_id": sid,
                "name": s.get("name", ""),
                "host_ip": host_ip,
                "status": s.get("status", ""),
                "healthy": healthy,
                "qemu_ports": qemu_ports,
            })
        return result

    def _print_pool(self, label: str, items: list, max_count: int) -> None:
        healthy = sum(1 for i in items if i["healthy"])
        self.log_info("%s: %d/%d servers (%d healthy)", label, len(items), max_count, healthy)
        for item in items:
            icon = "✓" if item["healthy"] else "✗"
            sid = item["server_id"][:12] if item["server_id"] else "N/A"
            self.log_info("  %s %s  %s  ports=%s",
                          icon, sid, item["host_ip"] or "no-ip", item["qemu_ports"])