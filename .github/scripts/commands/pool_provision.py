# -*- coding: utf-8 -*-
"""pool-provision command: idempotent creation / replenishment of dual-pool environments."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from core.base import BaseCommand
from pool.core import (
    POOL_A_PREFIX, POOL_A_MAX, POOL_A_SKU, POOL_A_QEMU_NUM,
    POOL_B_PREFIX, POOL_B_MAX, POOL_B_SKU, POOL_B_QEMU_NUM,
    _create_env, _list_servers, _compute_image_hash, _get_image_url,
    _delete_env,
)

logger = logging.getLogger("ci_cli.commands.pool_provision")


class PoolProvisionCommand(BaseCommand):
    """Idempotently create / replenish the CI pre-provisioned environment pools"""

    name = "pool-provision"
    description = "Idempotently create/replenish CI pre-provisioned pools (PoolA=1QEMU×20, PoolB=2QEMU×5)"

    def setup_parser(self, parser):
        parser.add_argument("--output", default="pool_info.json",
                            help="Output pool info JSON path")
        parser.add_argument("--image-work-dir", default="/tmp",
                            help="Image hash cache directory")

    def run(self, args) -> int:
        image_url = _get_image_url()
        if not image_url:
            self.log_error("No riscv_image_url found in Env")
            return 1

        # Image version detection
        current_hash = _compute_image_hash(image_url, args.image_work_dir)
        if not current_hash:
            self.log_error("Failed to compute image hash")
            return 1

        # Read previously recorded version
        from pool.core import _load_meta, _save_meta
        meta = _load_meta()
        saved_hash = meta.get("image_hash", "")
        if saved_hash and saved_hash != current_hash:
            self.log_info("Image hash changed (%s -> %s), rebuilding ALL pools",
                          saved_hash[:16], current_hash[:16])
            self._rebuild_pool("A", POOL_A_PREFIX)
            self._rebuild_pool("B", POOL_B_PREFIX)
        meta["image_hash"] = current_hash
        _save_meta(meta)

        # Replenish pool A
        self._fill_pool("A", POOL_A_PREFIX, POOL_A_MAX, POOL_A_QEMU_NUM, POOL_A_SKU)
        # Replenish pool B
        self._fill_pool("B", POOL_B_PREFIX, POOL_B_MAX, POOL_B_QEMU_NUM, POOL_B_SKU)

        # Output pool info
        pool_info = {
            "image_hash": current_hash,
            "pool_a": self._pool_status(POOL_A_PREFIX),
            "pool_b": self._pool_status(POOL_B_PREFIX),
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(pool_info, f, ensure_ascii=False, indent=2)
        self.log_info("Pool provision complete")
        return 0

    def _fill_pool(self, label: str, prefix: str, max_count: int,
                   qemu_num: int, sku: str) -> None:
        servers = _list_servers(prefix)
        current = len(servers)
        need = max_count - current
        if need <= 0:
            self.log_info("Pool %s: %d/%d OK", label, current, max_count)
            return
        self.log_info("Pool %s: %d/%d, creating %d more ...", label, current, max_count, need)
        for i in range(need):
            env = _create_env(qemu_num, sku, prefix)
            if env:
                self.log_info("Pool %s: created %d/%d", label, current + i + 1, max_count)
            else:
                self.log_error("Pool %s: create failed (%d/%d)", label, i + 1, need)

    def _rebuild_pool(self, label: str, prefix: str) -> None:
        servers = _list_servers(prefix)
        self.log_info("Rebuilding pool %s (%d servers) ...", label, len(servers))
        for s in servers:
            sid = s.get("id", "")
            if sid:
                _delete_env(sid)

    def _pool_status(self, prefix: str) -> dict:
        servers = _list_servers(prefix)
        return {"prefix": prefix, "count": len(servers),
                "ids": [s["id"][:12] for s in servers if s.get("id")]}