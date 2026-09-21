# -*- coding: utf-8 -*-
"""
cleanup-cloudpods command

Pipeline step 6: Clean up CloudPods cloud platform VMs created by the pipeline (regardless of success/failure).

Input: vm_info.json (contains server_ids)
Depends on: core.cloudpods.CloudPodsClient (reuses credentials)
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List

from core.base import BaseCommand
from core.cloudpods import CloudPodsClient, decrypt_password
from core.config import get_env

logger = logging.getLogger("ci_cli.commands.cleanup_cloudpods")


class CleanupCloudpodsCommand(BaseCommand):
    """Delete CloudPods VMs created by the pipeline"""

    name = "cleanup-cloudpods"
    description = "Delete CloudPods VMs created by the pipeline based on vm_info.json"

    def setup_parser(self, parser):
        parser.add_argument("--vm-info", required=True, help="Path to vm_info.json")

    def run(self, args) -> int:
        vm_info_path = Path(args.vm_info)
        if not vm_info_path.exists():
            self.log_error(f"vm_info.json not found: {vm_info_path}")
            return 1

        with open(vm_info_path, encoding="utf-8") as f:
            vm_info = json.load(f)

        server_ids: List[str] = vm_info.get("server_ids", [])
        # Defensive: some versions may wrap in quotes (e.g. 'uuid'), strip them uniformly
        server_ids = [str(s).strip().strip("'\"").strip() for s in server_ids if str(s).strip()]
        if not server_ids:
            self.log_info("No server_ids to clean up")
            return 0

        # Credentials: env vars first, then vm_info (written during launch)
        keystone_url = get_env("CLOUDPODS_KEYSTONE_URL") or vm_info.get("cloudpods_keystone_url", "")
        username = get_env("CLOUDPODS_USER") or vm_info.get("cloudpods_user", "")
        password_enc = get_env("CLOUDPODS_PASSWORD") or vm_info.get("cloudpods_password", "")

        if not keystone_url or not username or not password_enc:
            self.log_error("Missing CloudPods credentials "
                           "(CLOUDPODS_KEYSTONE_URL / CLOUDPODS_USER / CLOUDPODS_PASSWORD)")
            return 1

        # Password may be decrypted (plaintext) or still encrypted: try decrypt, fall back to raw
        password = password_enc
        try:
            password = decrypt_password(password_enc)
        except Exception:  # noqa: BLE001
            password = password_enc

        cp = CloudPodsClient(keystone_url=keystone_url, username=username, password=password)
        if cp._session is None:
            self.log_error("Failed to authenticate with CloudPods")
            return 1

        ok = True
        for sid in server_ids:
            self.log_info(f"Deleting server {sid}...")
            if cp.delete_server(sid):
                self.log_info(f"  {sid} deleted")
                cp.wait_for_server_is_deleted(sid, timeout=600)
            else:
                self.log_error(f"  {sid} delete failed")
                ok = False
        return 0 if ok else 1
