# -*- coding: utf-8 -*-
"""
launch-qemu-env 命令

流水线步骤 3：根据 compute-requirements 输出的规格 JSON，在 CloudPods 上
创建 KVM 虚拟机并在其中启动 openRuyi RISC-V QEMU 虚拟机。

实现方式：直接 import scripts/cloudpods/create_server.py（复制进来的库），
用规格 JSON 覆盖 Env 类的属性，再调用 create_qemu_server() 主流程。
随后解析日志输出，提取 host IP / QEMU SSH 端口 / 凭据写入 vm_info.json。

用法：
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
    """把规格 JSON 覆盖到 Env 类属性上，返回实际生效的字段列表。"""
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
            # create_server.py 中 riscv_qemu_disks 是 JSON 字符串（如 '[20,20]'）
            if env_attr == "riscv_qemu_disks":
                if isinstance(val, str):
                    pass  # 已是 JSON 字符串，原样传入
                elif isinstance(val, list):
                    val = json.dumps(val)
                else:
                    val = str(val)
            setattr(env_cls, env_attr, val)
            applied.append(env_attr)
    return applied


def parse_hosts_from_log(log_text: str) -> dict:
    """
    从 create_qemu_server 的日志中解析 host/QEMU 信息。
    日志格式（create_server.py 结尾输出）：
      CloudPods Server ID(s): [uuid1, uuid2]
      Total 1 host(s), 2 QEMU VM(s)
      --- Host 0: 10.20.40.x ---
        QEMU VM 0: ssh -p 12055 openruyi@10.20.40.x
        Bridge IPs (for inter-QEMU SSH on this host): 10.0.0.11, 10.0.0.21
    """
    result = {"hosts": [], "server_ids": [], "raw_log_tail": log_text[-3000:]}

    # server IDs（create_server.py 日志格式为 ['uuid1', 'uuid2']，含引号需剥掉）
    m = re.search(r"CloudPods Server ID\(s\):\s*\[([^\]]*)\]", log_text)
    if m:
        ids = [x.strip().strip("'\"").strip() for x in m.group(1).split(",") if x.strip()]
        result["server_ids"] = ids
    else:
        # 失败路径：末尾不会打印 CloudPods Server ID(s):，回退到创建时的行
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

        # server id per host（按顺序对应）
        server_id = result["server_ids"][idx] if idx < len(result["server_ids"]) else ""

        result["hosts"].append({
            "host_ip": host_ip,
            "server_id": server_id,
            "qemu_ports": ports,
            "qemu_bridge_ips": bridge_ips,
        })

    return result


def launch_env(spec: dict, logger=None, iscas_disable: bool = True) -> dict:
    """在 CloudPods 上创建一套 QEMU 环境（1 host + 若干 QEMU VM）。

    可直接被 CLI 命令或 functional 模块复用。返回 vm_info 字典：
      {
        "hosts": [{"host_ip", "server_id", "qemu_ports", "qemu_bridge_ips",
                   "ssh_user", "ssh_password", "host_ssh_user", "host_ssh_password"}],
        "server_ids": [...],
        "spec": {...},
        "ok": bool,
      }
    """
    # 直接 import 复制进来的 create_server 库（不再动态加载）
    from cloudpods import create_server as cs

    env_cls = cs.Env

    # ------------------------------------------------------------
    # 主机侧 yum 仓库修复（不修改 create_server.py）：
    #   ISCAS 镜像的 EPOL 仓库路径 404（正确是 EPOL/main/），且
    #   Everything 仓库极慢（~35KB/s），会导致 dnf makecache 失败。
    #   通过 monkey-patch SSHClient.exec 拦截 iscas-mirror.repo 的
    #   写入，将 enabled=1 全部改为 enabled=0（禁用 ISCAS 仓库），
    #   makecache 走默认 openEuler.repo 的 baseurl
    #   （repo.openeuler.org，已验证 200 且速度快）。
    # ------------------------------------------------------------
    if iscas_disable:
        orig_exec = cs.SSHClient.exec

        def patched_exec(self, cmd, timeout=60):
            if "iscas-mirror.repo" in cmd and "tee" in cmd:
                cmd = cmd.replace("enabled=1", "enabled=0")
                print("[launch-qemu-env] Disabled ISCAS mirror repos (EPOL 404 workaround)")
            return orig_exec(self, cmd, timeout)

        cs.SSHClient.exec = patched_exec

    # 环境变量优先（runner 机器上注入的 CloudPods 凭据）
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

    # 捕获 create_server 的日志输出
    log_capture = io.StringIO()
    log_handler = logging.StreamHandler(log_capture)
    log_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    cs.log.addHandler(log_handler)

    # 同时让原 logger 输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    cs.log.addHandler(console_handler)

    ok = cs.create_qemu_server(env_cls)

    # 获取捕获的日志
    captured = log_capture.getvalue()
    cs.log.removeHandler(log_handler)
    cs.log.removeHandler(console_handler)

    if not ok:
        if logger:
            logger.error(f"create_qemu_server FAILED, tail of log:\n{captured[-3000:]}")
        # 仍然尝试解析已创建的服务器用于清理
        info = parse_hosts_from_log(captured)
        return {**info, "spec": spec, "ok": False}

    info = parse_hosts_from_log(captured)
    if not info["hosts"]:
        if logger:
            logger.error("No hosts parsed from log, parsing failed")
            logger.error(captured[-5000:])
        return {**info, "spec": spec, "ok": False}

    # 补充凭据信息（从 Env）
    for host in info["hosts"]:
        host["ssh_user"] = env_cls.riscv_default_username
        host["ssh_password"] = env_cls.riscv_default_password
        host["host_ssh_user"] = env_cls.cloudpods_server_user
        host["host_ssh_password"] = env_cls.cloudpods_server_password

    vm_info = {**info, "spec": spec, "ok": True}

    # 补充 CloudPods 凭据（供 cleanup-cloudpods 无环境变量时回退）
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
    """创建 CloudPods 主机并在其中启动 QEMU 虚拟机"""

    name = "launch-qemu-env"
    description = "在 CloudPods 创建 KVM 主机并启动 openRuyi RISC-V QEMU 虚拟机"

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
