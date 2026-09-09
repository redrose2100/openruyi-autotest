#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_requirements.py

流水线步骤 2：根据 PR 中 tests/ 目录下改动的文件，解析其所属测试套/用例的
FMF 元数据（extra-hardware-require 继承链 + require 包列表 + tier），
计算在 CloudPods 上创建 openRuyi QEMU 虚拟机所需的资源规格。

输出（JSON）：
  {
    "test_paths":  ["/tests/functional/pkgs/acl/test_acl_getfacl_basic", ...],
    "suite_paths": ["/tests/functional/pkgs/acl", ...],
    "spec": {
      "cloudpods_server_num": 1,     # CloudPods KVM 虚拟机数量
      "riscv_qemu_num": 2,           # 每台 KVM 内 QEMU RISC-V VM 数量
      "riscv_qemu_cpu": 8,           # 每个 QEMU 的 CPU 核数
      "riscv_qemu_memory": 8,        # 每个 QEMU 的内存 GB
      "riscv_qemu_net_num": 1,       # 每个 QEMU 额外网卡数
      "riscv_qemu_disks": "[20]",    # 每个 QEMU 额外数据盘（JSON 数组）
      "server_sku": "ecs.g1.c16m16", # CloudPods SKU
      "packages": ["acl", "beakerlib"],   # 需要在 QEMU 内安装的包
      "reason": "..."                # 资源计算说明
    }
  }
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ============================================================
# 默认资源规格（无显式需求时的基准值）
# ============================================================
DEFAULT_SPEC = {
    "cloudpods_server_num": 1,
    "riscv_qemu_num": 1,
    "riscv_qemu_cpu": 4,
    "riscv_qemu_memory": 4,
    "riscv_qemu_net_num": 1,
    "riscv_qemu_disks": "[]",
    "server_sku": "ecs.g1.c8m8",
}

# 需要更多资源的测试类型规则（按路径关键字匹配）
EXTRA_RESOURCE_RULES = [
    {
        "pattern": r"performance|unixbench|mmtests|fio|iozone|stream|lmbench|sysbench",
        "cpu": 8, "memory": 8, "qemu_num": 1, "net": 0, "disk": 0,
        "reason": "性能基准测试需要更多 CPU/内存",
    },
    {
        "pattern": r"compatibility/ltp_posix",
        "cpu": 4, "memory": 4, "qemu_num": 1, "net": 0, "disk": 0,
        "reason": "LTP POSIX 兼容性测试",
    },
    {
        "pattern": r"reliability/stress-ng|reliability/trinity",
        "cpu": 8, "memory": 8, "qemu_num": 1, "net": 0, "disk": 0,
        "reason": "压力测试需要更多资源",
    },
    {
        "pattern": r"feature/k8s",
        "cpu": 8, "memory": 16, "qemu_num": 1, "net": 1, "disk": 20,
        "reason": "K8s 集群测试需要较多资源",
    },
]

# QEMU 数量分档（用例多时拆分为多台 QEMU 并行）
QEMU_NUM_TIERS = [(0, 1), (5, 2), (10, 4), (20, 8)]

# 允许覆盖的 Env 属性（launch_qemu_env.py 会据此注入）
SPEC_KEYS = [
    "cloudpods_server_num",
    "riscv_qemu_num",
    "riscv_qemu_cpu",
    "riscv_qemu_memory",
    "riscv_qemu_net_num",
    "riscv_qemu_disks",
    "server_sku",
]


def find_fmf_ancestors(test_dir: Path) -> List[Path]:
    """向上查找包含 main.fmf 的目录链（从最近的测试目录到 tests/ 根）"""
    ancestors = []
    cur = test_dir
    while True:
        fmf = cur / "main.fmf"
        if fmf.exists():
            ancestors.append(fmf)
        if cur.name == "tests" or cur.parent == cur:
            break
        cur = cur.parent
    return ancestors


def parse_fmf_value(raw: str) -> str:
    """清理 fmf 字段值中的引号/注释"""
    raw = raw.strip()
    raw = re.sub(r"#.*$", "", raw).strip()
    raw = raw.strip('"').strip("'")
    return raw


def parse_hardware_require(fmf_files: List[Path]) -> Dict[str, str]:
    """沿继承链（子 -> 父）解析 extra-hardware-require 各字段，合并返回"""
    hw: Dict[str, str] = {}
    for fmf in fmf_files:
        try:
            lines = fmf.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        in_section = False
        for line in lines:
            if re.match(r"^\s*extra-hardware-require\s*:", line):
                in_section = True
                continue
            if in_section:
                if re.match(r"^\s+[a-z]", line):
                    m = re.match(r"^\s+([a-z]+)\s*:\s*(.*)$", line)
                    if m:
                        key, val = m.group(1), parse_fmf_value(m.group(2))
                        if val:
                            hw.setdefault(key, val)
                elif re.match(r"^[^\s]", line):
                    break
    return hw


def parse_require(fmf_files: List[Path]) -> List[str]:
    """收集 require 中的包名（排除 /path 形式，即排除依赖用例）"""
    pkgs: Set[str] = set()
    for fmf in fmf_files:
        try:
            lines = fmf.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        in_require = False
        for line in lines:
            if re.match(r"^\s*require\s*:", line):
                in_require = True
                continue
            if in_require:
                if re.match(r"^\s*-\s+", line):
                    val = parse_fmf_value(re.sub(r"^\s*-\s+", "", line))
                    if val and not val.startswith("/"):
                        pkgs.add(val)
                elif re.match(r"^\s+[a-zA-Z]", line):
                    val = parse_fmf_value(line)
                    if val and not val.startswith("/") and ":" not in val:
                        pkgs.add(val)
                elif re.match(r"^[^\s]", line):
                    break
    return sorted(pkgs)


def parse_num(raw: str, default: int) -> int:
    """把 '>= 4' / '4' / '8 GiB' 等解析为整数"""
    if not raw:
        return default
    m = re.search(r"(\d+)", raw)
    return int(m.group(1)) if m else default


# CloudPods 平台实际存在的规格（从 /serverskus 查询，2026-09-09）
# cpu: [内存 GB 列表]
AVAILABLE_SKU_MEM_BY_CPU = {
    1: [1, 2, 4, 8],
    2: [2, 4, 8, 12, 16],
    4: [4, 12, 16, 24, 32],
    8: [8, 16, 24, 32, 64, 96],
    12: [12, 16, 24, 32, 64],
    16: [16, 24, 32, 48, 64, 192],
    24: [24, 32, 48, 64, 128],
    32: [32, 48, 64, 128],
    128: [256],
}

# 平台可用的 CPU 核数（升序）
AVAILABLE_CPU = sorted(AVAILABLE_SKU_MEM_BY_CPU.keys())


def pick_sku(cpu: int, memory: int) -> str:
    """根据总 CPU/内存需求选择平台上真实存在的 SKU（ecs.g1.cXmY）"""
    # 找 >= 需求的 CPU 核数（平台实际规格）
    sku_cpu = None
    for c in AVAILABLE_CPU:
        if c >= cpu:
            sku_cpu = c
            break
    if sku_cpu is None:
        sku_cpu = AVAILABLE_CPU[-1]
    # 找 >= 需求的内存（GB）的规格
    mems = AVAILABLE_SKU_MEM_BY_CPU[sku_cpu]
    sku_mem = None
    for m in mems:
        if m >= memory:
            sku_mem = m
            break
    if sku_mem is None:
        sku_mem = mems[-1]
    return f"ecs.g1.c{sku_cpu}m{sku_mem}"


def compute_spec(changed_files: List[str], repo_root: Path) -> Tuple[List[str], List[str], Dict]:
    """核心：从改动文件列表计算测试路径与资源规格"""
    tests_root = repo_root / "tests"

    test_paths: List[str] = []
    suite_paths: List[str] = []
    all_fmf_files: List[Path] = []
    all_pkgs: Set[str] = set()
    matched_rules: List[Dict] = []
    case_count = 0

    for rel in changed_files:
        # 规范化相对路径
        rel = rel.strip()
        if not rel:
            continue
        path = tests_root / rel if not rel.startswith("tests/") else repo_root / rel
        if not path.exists():
            continue

        # 定位到该文件所属的测试目录
        test_dir = path if path.is_dir() else path.parent

        fmf_files = find_fmf_ancestors(test_dir)
        if not fmf_files:
            continue
        all_fmf_files.extend(fmf_files)

        # 判断是"用例"还是"测试套"
        is_case = (test_dir / "test.sh").exists()
        if is_case:
            case_count += 1

        # 找到 fmf path（从 main.fmf 的 path: 字段或目录推算）
        own_fmf = test_dir / "main.fmf"
        fmf_path = ""
        if own_fmf.exists():
            for line in own_fmf.read_text(encoding="utf-8", errors="replace").splitlines():
                if re.match(r"^\s*path\s*:", line):
                    fmf_path = parse_fmf_value(line.split(":", 1)[1])
                    break
        if not fmf_path:
            try:
                fmf_path = "/" + test_dir.relative_to(repo_root).as_posix()
            except ValueError:
                fmf_path = "/" + str(test_dir)

        # 收集资源需求
        pkgs = parse_require(fmf_files)
        all_pkgs.update(pkgs)

        # 追加到对应列表
        if is_case:
            test_paths.append(fmf_path)
        else:
            suite_paths.append(fmf_path)

        # 检查扩展资源规则
        path_str = fmf_path
        for rule in EXTRA_RESOURCE_RULES:
            if re.search(rule["pattern"], path_str, re.IGNORECASE):
                if rule not in matched_rules:
                    matched_rules.append(rule)

    # 去重并排序
    test_paths = sorted(set(test_paths))
    suite_paths = sorted(set(suite_paths))
    if not test_paths and not suite_paths:
        return [], [], {**DEFAULT_SPEC, "packages": [], "reason": "no test dirs found",
                        "test_paths": [], "suite_paths": []}

    # ---- 计算资源规格 ----
    cpu = DEFAULT_SPEC["riscv_qemu_cpu"]
    memory = DEFAULT_SPEC["riscv_qemu_memory"]
    net = DEFAULT_SPEC["riscv_qemu_net_num"]
    disk = 0
    qemu_num = DEFAULT_SPEC["riscv_qemu_num"]

    # 从 FMF 继承链中取最大需求
    for fmf in all_fmf_files:
        hw = parse_hardware_require([fmf])
        cpu = max(cpu, parse_num(hw.get("cpu"), DEFAULT_SPEC["riscv_qemu_cpu"]))
        memory = max(memory, parse_num(hw.get("memory"), DEFAULT_SPEC["riscv_qemu_memory"]))
        net = max(net, parse_num(hw.get("net"), DEFAULT_SPEC["riscv_qemu_net_num"]))
        disk = max(disk, parse_num(hw.get("disk"), 0))

    # 扩展规则加成（取最大的）
    for rule in matched_rules:
        cpu = max(cpu, rule["cpu"])
        memory = max(memory, rule["memory"])
        qemu_num = max(qemu_num, rule["qemu_num"])
        disk = max(disk, rule["disk"])
        net = max(net, rule["net"])

    # 数据盘：每个 20G
    disk_sizes = [20] * disk if disk > 0 else []

    # QEMU 数量分档（用例多时拆分为多台 QEMU）
    total_items = len(test_paths) + len(suite_paths)
    for threshold, num in QEMU_NUM_TIERS:
        if total_items > threshold:
            qemu_num = max(qemu_num, num)

    # SKU 选择（确保能承载 cpu*qemu_num / memory*qemu_num）
    total_cpu = cpu * qemu_num
    total_mem = memory * qemu_num
    sku = pick_sku(total_cpu, total_mem)

    reason_parts = [f"{total_items} 个测试目录"]
    if matched_rules:
        reason_parts.append("; ".join(r["reason"] for r in matched_rules))

    spec = {
        "cloudpods_server_num": 1,
        "riscv_qemu_num": qemu_num,
        "riscv_qemu_cpu": cpu,
        "riscv_qemu_memory": memory,
        "riscv_qemu_net_num": net,
        "riscv_qemu_disks": json.dumps(disk_sizes),
        "server_sku": sku,
        "packages": sorted(all_pkgs),
        "reason": "; ".join(reason_parts),
    }
    return test_paths, suite_paths, spec


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute CloudPods QEMU VM requirements from changed test files")
    ap.add_argument("--repo", required=True, help="Repository root path")
    ap.add_argument("--changed-files", required=True, help="File listing changed files under tests/")
    ap.add_argument("--output", required=True, help="Output JSON path")
    args = ap.parse_args()

    repo_root = Path(args.repo).resolve()
    with open(args.changed_files, encoding="utf-8") as f:
        changed_files = [ln.strip() for ln in f if ln.strip()]

    if not changed_files:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"test_paths": [], "suite_paths": [], "spec": {}}, f, ensure_ascii=False, indent=2)
        print("No changed files")
        return 0

    test_paths, suite_paths, spec = compute_spec(changed_files, repo_root)

    result = {
        "test_paths": test_paths,
        "suite_paths": suite_paths,
        "spec": spec,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"test_paths: {test_paths}")
    print(f"suite_paths: {suite_paths}")
    print(f"spec: {json.dumps(spec, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
