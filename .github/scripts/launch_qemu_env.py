#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
launch_qemu_env.py

流水线步骤 3：根据 compute_requirements.py 输出的规格 JSON，
在 CloudPods 上创建 KVM 虚拟机并在其中启动 openRuyi RISC-V QEMU 虚拟机。

实现方式：
  不修改 tools/cloudpods/create_server.py，而是通过 importlib 动态加载它，
  用规格 JSON 覆盖 Env 类的属性，再调用 create_qemu_server() 主流程。
  随后解析日志输出，提取 host IP / QEMU SSH 端口 / 凭据写入 vm_info.json。

输出（JSON）：
  {
    "hosts": [
      {
        "host_ip": "10.20.40.x",
        "server_id": "xxx",
        "qemu_ports": [12055, 12056],
        "qemu_bridge_ips": ["10.0.0.11", "10.0.0.21"],
        "ssh_user": "openruyi",
        "ssh_password": "openruyi",
        "host_ssh_user": "root",
        "host_ssh_password": "ISRCpassword@123"
      }
    ],
    "spec": {...}   # 回显使用的规格
  }
"""

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

# 保证可以 import tools 下的模块（如果 create_server.py 依赖同级模块）
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # 仓库根目录


def load_create_server_module(create_server_path: Path):
    """动态加载 create_server.py 模块，不修改原文件"""
    spec = importlib.util.spec_from_file_location(
        "create_server", str(create_server_path)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def apply_spec_to_env(env_cls, spec: dict) -> list:
    """把规格 JSON 覆盖到 Env 类属性上，返回实际生效的字段列表"""
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
                    # 已是 JSON 字符串，原样传入
                    pass
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
    result = {
        "hosts": [],
        "server_ids": [],
        "raw_log_tail": log_text[-3000:],
    }

    # server IDs
    m = re.search(r"CloudPods Server ID\(s\):\s*\[([^\]]*)\]", log_text)
    if m:
        ids = [x.strip() for x in m.group(1).split(",") if x.strip()]
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

        # server id per host (按顺序对应)
        server_id = result["server_ids"][idx] if idx < len(result["server_ids"]) else ""

        result["hosts"].append({
            "host_ip": host_ip,
            "server_id": server_id,
            "qemu_ports": ports,
            "qemu_bridge_ips": bridge_ips,
        })

    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Launch CloudPods hosts and QEMU VMs")
    ap.add_argument("--requirements", required=True, help="Path to vm_requirements.json")
    ap.add_argument("--output", required=True, help="Output vm_info.json path")
    ap.add_argument("--create-server", default=None,
                    help="Path to create_server.py (default: tools/cloudpods/create_server.py)")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    req_path = Path(args.requirements)
    with open(req_path, encoding="utf-8") as f:
        req = json.load(f)

    spec = req.get("spec", {})
    if not spec:
        print("Empty spec, nothing to launch")
        return 0

    create_server_path = Path(args.create_server) if args.create_server else (
        repo_root / "tools" / "cloudpods" / "create_server.py"
    )
    if not create_server_path.exists():
        print(f"create_server.py not found: {create_server_path}")
        return 1

    # 动态加载 create_server.py
    mod = load_create_server_module(create_server_path)
    env_cls = mod.Env

    # 环境变量优先（runner 机器上注入的 CloudPods 凭据）
    for env_key, attr in [
        ("CLOUDPODS_KEYSTONE_URL", "cloudpods_keystone_url"),
        ("CLOUDPODS_USER", "cloudpods_user"),
        ("CLOUDPODS_PASSWORD", "cloudpods_password"),
    ]:
        if os.environ.get(env_key):
            setattr(env_cls, attr, os.environ[env_key])

    applied = apply_spec_to_env(env_cls, spec)
    print(f"Applied spec fields to Env: {applied}")

    # 调用主流程（日志同时打印到 stdout 和捕获）
    import io
    import logging

    # 捕获 create_server 的日志输出
    log_capture = io.StringIO()
    log_handler = logging.StreamHandler(log_capture)
    log_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    mod.log.addHandler(log_handler)

    # 同时让原 logger 输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    mod.log.addHandler(console_handler)

    ok = mod.create_qemu_server(env_cls)

    # 获取捕获的日志
    captured = log_capture.getvalue()
    mod.log.removeHandler(log_handler)
    mod.log.removeHandler(console_handler)

    if not ok:
        print(f"create_qemu_server FAILED, tail of log:\n{captured[-3000:]}")
        # 仍然尝试解析已创建的服务器用于清理
        info = parse_hosts_from_log(captured)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({**info, "spec": spec, "ok": False}, f, ensure_ascii=False, indent=2)
        return 1

    info = parse_hosts_from_log(captured)
    if not info["hosts"]:
        print("No hosts parsed from log, parsing failed")
        print(captured[-5000:])
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({**info, "spec": spec, "ok": False}, f, ensure_ascii=False, indent=2)
        return 1

    # 补充凭据信息（从 Env）
    for host in info["hosts"]:
        host["ssh_user"] = env_cls.riscv_default_username
        host["ssh_password"] = env_cls.riscv_default_password
        host["host_ssh_user"] = env_cls.cloudpods_server_user
        host["host_ssh_password"] = env_cls.cloudpods_server_password

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump({**info, "spec": spec, "ok": True}, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"Launched {len(info['hosts'])} host(s), total QEMU VMs: "
          f"{sum(len(h['qemu_ports']) for h in info['hosts'])}")
    for h in info["hosts"]:
        print(f"  Host {h['host_ip']}: QEMU ports={h['qemu_ports']}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
