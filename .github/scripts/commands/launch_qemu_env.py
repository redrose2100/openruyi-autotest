# -*- coding: utf-8 -*-
"""
launch-qemu-env command

Pipeline step 3: Based on the spec JSON output by compute-requirements, create
KVM VMs on CloudPods and launch openRuyi RISC-V QEMU VMs inside them.

Implementation: directly import scripts/cloudpods/create_server.py (the copied-in
library), override Env class properties with the spec JSON, then call the
create_qemu_server() main workflow.
Afterwards parse log output, extract host IP / QEMU SSH port / credentials
and write them to vm_info.json.

Usage:
  python3 .github/scripts/cli.py launch-qemu-env \
      --requirements vm_requirements.json --output vm_info.json
"""
from __future__ import annotations

import argparse
import io
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Optional

from core.base import BaseCommand

logger = logging.getLogger("ci_cli.commands.launch_qemu_env")


def apply_spec_to_env(env_cls, spec: dict) -> list:
    """Apply spec JSON to Env class properties, return list of fields actually set."""
    applied = []
    mapping = {
        "cloudpods_server_num": "cloudpods_server_num",
        "riscv_qemu_num": "riscv_qemu_num",
        "riscv_qemu_cpu": "riscv_qemu_cpu",
        "riscv_qemu_memory": "riscv_qemu_memory",
        "riscv_qemu_net_num": "riscv_qemu_net_num",
        "riscv_qemu_disks": "riscv_qemu_disks",
        "server_sku": "server_sku",
        "cloudpods_keystone_url": "cloudpods_keystone_url",
        "cloudpods_user": "cloudpods_user",
        "cloudpods_password": "cloudpods_password",
    }
    for spec_key, env_attr in mapping.items():
        if spec_key in spec and spec[spec_key] is not None and spec[spec_key] != "":
            val = spec[spec_key]
            # In create_server.py, riscv_qemu_disks is a JSON string (e.g. '[20,20]')
            if env_attr == "riscv_qemu_disks":
                if isinstance(val, str):
                    pass  # Already a JSON string, pass through as-is
                elif isinstance(val, list):
                    val = json.dumps(val)
                else:
                    val = str(val)
            setattr(env_cls, env_attr, val)
            applied.append(env_attr)
    return applied


def parse_hosts_from_log(log_text: str) -> dict:
    """
    Parse host/QEMU info from create_qemu_server log output.
    Log format (create_server.py final output):
      CloudPods Server ID(s): [uuid1, uuid2]
      Total 1 host(s), 2 QEMU VM(s)
      --- Host 0: 10.20.40.x ---
        QEMU VM 0: ssh -p 12055 openruyi@10.20.40.x
        Bridge IPs (for inter-QEMU SSH on this host): 10.0.0.11, 10.0.0.21
    """
    result = {"hosts": [], "server_ids": [], "raw_log_tail": log_text[-3000:]}

    # server IDs (create_server.py log format is ['uuid1', 'uuid2'], strip quotes)
    m = re.search(r"CloudPods Server ID\(s\):\s*\[([^\]]*)\]", log_text)
    if m:
        ids = [x.strip().strip("'\"").strip() for x in m.group(1).split(",") if x.strip()]
        result["server_ids"] = ids
    else:
        # Failure path: final output won't include CloudPods Server ID(s):, fall back to creation-time line
        m2 = re.search(r"Created servers:\s*\[([^\]]*)\]", log_text)
        if m2:
            ids = [x.strip().strip("'\"").strip() for x in m2.group(1).split(",") if x.strip()]
            result["server_ids"] = ids

    # host blocks: "--- Host N: ip ---"
    host_blocks = list(re.finditer(r"--- Host \d+: ([0-9.]+) ---", log_text))
    for idx, hm in enumerate(host_blocks):
        host_ip = hm.group(1)
        start = hm.end()
        end = host_blocks[idx + 1].start() if idx + 1 < len(host_blocks) else len(log_text)
        block = log_text[start:end]

        # QEMU ports
        ports = [int(p) for p in re.findall(r"ssh -p (\d+)", block)]
        # bridge IPs
        bm = re.search(r"Bridge IPs .*?:\s*([0-9., ]+)", block)
        bridge_ips = []
        if bm:
            bridge_ips = [x.strip() for x in bm.group(1).split(",") if x.strip()]

        # server id per host (in order)
        server_id = result["server_ids"][idx] if idx < len(result["server_ids"]) else ""

        result["hosts"].append({
            "host_ip": host_ip,
            "server_id": server_id,
            "qemu_ports": ports,
            "qemu_bridge_ips": bridge_ips,
        })

    return result


def launch_env(spec: dict, logger=None, iscas_disable: bool = True) -> dict:
    """Create a QEMU environment on CloudPods (1 host + several QEMU VMs).

    Can be reused directly by CLI commands or the functional module. Returns a vm_info dict:
      {
        "hosts": [{"host_ip", "server_id", "qemu_ports", "qemu_bridge_ips",
                   "ssh_user", "ssh_password", "host_ssh_user", "host_ssh_password"}],
        "server_ids": [...],
        "spec": {...},
        "ok": bool,
      }
    """
    # Directly import the copied-in create_server library (no more dynamic loading)
    from cloudpods import create_server as cs

    env_cls = cs.Env

    # ------------------------------------------------------------
    # Host-side yum repo fix (without modifying create_server.py):
    #   The ISCAS mirror EPOL repo path returns 404 (the correct path is EPOL/main/),
    #   and the Everything repo is extremely slow (~35KB/s), which causes
    #   dnf makecache to fail.
    #   Monkey-patch SSHClient.exec to intercept iscas-mirror.repo writes,
    #   changing enabled=1 to enabled=0 (disabling ISCAS repos),
    #   so makecache uses the default openEuler.repo baseurl
    #   (repo.openeuler.org, verified as 200 and fast).
    # ------------------------------------------------------------
    if iscas_disable:
        orig_exec = cs.SSHClient.exec

        def patched_exec(self, cmd, timeout=60):
            if "iscas-mirror.repo" in cmd and "tee" in cmd:
                cmd = cmd.replace("enabled=1", "enabled=0")
                print("[launch-qemu-env] Disabled ISCAS mirror repos (EPOL 404 workaround)")
            return orig_exec(self, cmd, timeout)

        cs.SSHClient.exec = patched_exec

    # Environment variables take priority (CloudPods credentials injected on the runner machine)
    for env_key, attr in [
        ("CLOUDPODS_KEYSTONE_URL", "cloudpods_keystone_url"),
        ("CLOUDPODS_USER", "cloudpods_user"),
        ("CLOUDPODS_PASSWORD", "cloudpods_password"),
    ]:
        if os.environ.get(env_key):
            setattr(env_cls, attr, os.environ[env_key])

    applied = apply_spec_to_env(env_cls, spec)
    if logger:
        logger.info(f"Applied spec fields to Env: {applied}")

    # Capture create_server log output
    log_capture = io.StringIO()
    log_handler = logging.StreamHandler(log_capture)
    log_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    cs.log.addHandler(log_handler)

    # Also attach console handler to original logger
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    cs.log.addHandler(console_handler)

    ok = cs.create_qemu_server(env_cls)

    # Get captured log output
    captured = log_capture.getvalue()
    cs.log.removeHandler(log_handler)
    cs.log.removeHandler(console_handler)

    if not ok:
        if logger:
            logger.error(f"create_qemu_server FAILED, tail of log:\n{captured[-3000:]}")
        # Still try to parse already-created servers for cleanup
        info = parse_hosts_from_log(captured)
        return {**info, "spec": spec, "ok": False}

    info = parse_hosts_from_log(captured)
    if not info["hosts"]:
        if logger:
            logger.error("No hosts parsed from log, parsing failed")
            logger.error(captured[-5000:])
        return {**info, "spec": spec, "ok": False}

    # Augment with credential info (from Env)
    for host in info["hosts"]:
        host["ssh_user"] = env_cls.riscv_default_username
        host["ssh_password"] = env_cls.riscv_default_password
        host["host_ssh_user"] = env_cls.cloudpods_server_user
        host["host_ssh_password"] = env_cls.cloudpods_server_password

    vm_info = {**info, "spec": spec, "ok": True}

    # Augment with CloudPods credentials (fallback for cleanup-cloudpods when env vars absent)
    vm_info["cloudpods_keystone_url"] = env_cls.cloudpods_keystone_url
    vm_info["cloudpods_user"] = env_cls.cloudpods_user
    vm_info["cloudpods_password"] = env_cls.cloudpods_password

    if logger:
        logger.info("=" * 60)
        logger.info(f"Launched {len(info['hosts'])} host(s), total QEMU VMs: "
                    f"{sum(len(h['qemu_ports']) for h in info['hosts'])}")
        for h in info["hosts"]:
            logger.info(f"  Host {h['host_ip']}: QEMU ports={h['qemu_ports']}")
        logger.info("=" * 60)
    return vm_info


class LaunchQemuEnvCommand(BaseCommand):
    """Create CloudPods hosts and launch QEMU VMs inside them"""

    name = "launch-qemu-env"
    description = "Create KVM hosts on CloudPods and launch openRuyi RISC-V QEMU VMs"

    def setup_parser(self, parser):
        parser.add_argument("--requirements", required=True, help="Path to vm_requirements.json")
        parser.add_argument("--output", required=True, help="Output vm_info.json path")

    def run(self, args) -> int:
        req_path = Path(args.requirements)
        with open(req_path, encoding="utf-8") as f:
            req = json.load(f)

        spec = req.get("spec", {})
        if not spec:
            self.log_info("Empty spec, nothing to launch")
            return 0

        vm_info = launch_env(spec, logger=logger)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(vm_info, f, ensure_ascii=False, indent=2)
        return 0 if vm_info.get("ok") else 1
