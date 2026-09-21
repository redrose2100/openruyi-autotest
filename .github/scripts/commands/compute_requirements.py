# -*- coding: utf-8 -*-
"""
compute-requirements command

Pipeline step 2: Based on changed files under tests/ in the PR, resolve their
FMF metadata (extra-hardware-require inheritance chain + require package list + tier),
and compute the resource spec needed to create openRuyi QEMU VMs on CloudPods.

Usage:
  python3 .github/scripts/cli.py compute-requirements \
      --repo <repo_root> --changed-files <file> --output <vm_requirements.json>
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from core.base import BaseCommand

# ------------------------------------------------------------
# Default resource spec (baseline when no explicit requirements)
# ------------------------------------------------------------
DEFAULT_SPEC = {
    "cloudpods_server_num": 1,
    "riscv_qemu_num": 1,
    "riscv_qemu_cpu": 4,
    "riscv_qemu_memory": 4,
    "riscv_qemu_net_num": 1,
    "riscv_qemu_disks": "[]",
    "server_sku": "ecs.g1.c8m8",
}

# Rules for test types needing more resources (matched by path keyword)
EXTRA_RESOURCE_RULES = [
    {
        "pattern": r"performance|unixbench|mmtests|fio|iozone|stream|lmbench|sysbench",
        "cpu": 8, "memory": 8, "qemu_num": 1, "net": 0, "disk": 0,
        "reason": "Performance benchmarks need more CPU/memory",
    },
    {
        "pattern": r"compatibility/ltp_posix",
        "cpu": 4, "memory": 4, "qemu_num": 1, "net": 0, "disk": 0,
        "reason": "LTP POSIX compatibility tests",
    },
    {
        "pattern": r"reliability/stress-ng|reliability/trinity",
        "cpu": 8, "memory": 8, "qemu_num": 1, "net": 0, "disk": 0,
        "reason": "Stress tests need more resources",
    },
    {
        "pattern": r"feature/k8s",
        "cpu": 8, "memory": 16, "qemu_num": 1, "net": 1, "disk": 20,
        "reason": "K8s cluster tests need much more resources",
    },
]

# QEMU count tiers (split into multiple QEMU instances when many test cases)
QEMU_NUM_TIERS = [(0, 1), (5, 2), (10, 4), (20, 8)]

# SKUs actually available on CloudPods platform (from /serverskus query, 2026-09-09)
# cpu: [memory GB list]
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

# Available CPU core counts on the platform (ascending)
AVAILABLE_CPU = sorted(AVAILABLE_SKU_MEM_BY_CPU.keys())


# ------------------------------------------------------------
# FMF metadata parsing utilities
# ------------------------------------------------------------
def find_fmf_ancestors(test_dir: Path) -> List[Path]:
    """Walk upward from the test directory to find the chain of directories containing main.fmf (up to tests/ root)."""
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
    """Clean quotes/comments from fmf field values."""
    raw = raw.strip()
    raw = re.sub(r"#.*$", "", raw).strip()
    raw = raw.strip('"').strip("'")
    return raw


def parse_server_require(test_dir: Path) -> int:
    """Nearest-match parsing of server: field (test dir -> upward traversal -> default 1).

    Starting from test_dir itself, search upward for server: field in main.fmf;
    use the first match found; return default 1 if none found.
    """
    cur = test_dir
    while True:
        fmf = cur / "main.fmf"
        if fmf.exists():
            try:
                content = fmf.read_text(encoding="utf-8", errors="replace")
                for line in content.splitlines():
                    m = re.match(r"^\s*server\s*:\s*(.+)$", line)
                    if m:
                        val = parse_fmf_value(m.group(1))
                        try:
                            n = int(val)
                            if n in (1, 2):
                                return n
                        except ValueError:
                            pass
            except Exception:
                pass
        if cur.name == "tests" or cur.parent == cur:
            break
        cur = cur.parent
    return 1  # default


def parse_hardware_require(fmf_files: List[Path]) -> Dict[str, str]:
    """Follow the inheritance chain (child -> parent) to parse extra-hardware-require fields and merge."""
    hw: Dict[str, str] = {}
    for fmf in fmf_files:
        try:
            lines = fmf.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:  # noqa: BLE001
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
    """Collect package names from require (exclude /path form, i.e. exclude dependent test cases)."""
    pkgs: Set[str] = set()
    for fmf in fmf_files:
        try:
            lines = fmf.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:  # noqa: BLE001
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
    """Parse strings like '>= 4' / '4' / '8 GiB' into integers."""
    if not raw:
        return default
    m = re.search(r"(\d+)", raw)
    return int(m.group(1)) if m else default


def pick_sku(cpu: int, memory: int) -> str:
    """Select a real SKU (ecs.g1.cXmY) from the platform based on total CPU/memory requirements."""
    sku_cpu = next((c for c in AVAILABLE_CPU if c >= cpu), AVAILABLE_CPU[-1])
    mems = AVAILABLE_SKU_MEM_BY_CPU[sku_cpu]
    sku_mem = next((m for m in mems if m >= memory), mems[-1])
    return f"ecs.g1.c{sku_cpu}m{sku_mem}"


def compute_spec(changed_files: List[str], repo_root: Path) -> Tuple[List[str], List[str], Dict]:
    """Core: compute test paths and resource spec from the list of changed files."""
    tests_root = repo_root / "tests"

    test_paths: List[str] = []
    suite_paths: List[str] = []
    all_fmf_files: List[Path] = []
    all_pkgs: Set[str] = set()
    matched_rules: List[Dict] = []
    case_count = 0

    for rel in changed_files:
        rel = rel.strip()
        if not rel:
            continue
        path = tests_root / rel if not rel.startswith("tests/") else repo_root / rel
        if not path.exists():
            continue

        # Locate the test directory this file belongs to
        test_dir = path if path.is_dir() else path.parent

        fmf_files = find_fmf_ancestors(test_dir)
        if not fmf_files:
            continue
        all_fmf_files.extend(fmf_files)

        # Determine whether it's a "test case" or a "test suite"
        is_case = (test_dir / "test.sh").exists()
        if is_case:
            case_count += 1

        # Find fmf path (from main.fmf path: field or derive from directory)
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

        # Collect resource requirements
        pkgs = parse_require(fmf_files)
        all_pkgs.update(pkgs)

        if is_case:
            test_paths.append(fmf_path)
        else:
            suite_paths.append(fmf_path)

        # Check extended resource rules
        for rule in EXTRA_RESOURCE_RULES:
            if re.search(rule["pattern"], fmf_path, re.IGNORECASE):
                if rule not in matched_rules:
                    matched_rules.append(rule)

    test_paths = sorted(set(test_paths))
    suite_paths = sorted(set(suite_paths))
    if not test_paths and not suite_paths:
        return [], [], {**DEFAULT_SPEC, "packages": [], "reason": "no test dirs found",
                        "test_paths": [], "suite_paths": [], "server_count": 1}

    # ---- Compute server_count (nearest-match, take global maximum) ----
    server_count = 1
    for rel in changed_files:
        rel = rel.strip()
        if not rel:
            continue
        path = tests_root / rel if not rel.startswith("tests/") else repo_root / rel
        if not path.exists():
            continue
        test_dir = path if path.is_dir() else path.parent
        sc = parse_server_require(test_dir)
        if sc > server_count:
            server_count = sc
    if server_count > 1:
        logger.info("Detected server_count=%d from fmf server: fields", server_count)

    # ---- Compute resource spec ----
    cpu = DEFAULT_SPEC["riscv_qemu_cpu"]
    memory = DEFAULT_SPEC["riscv_qemu_memory"]
    net = DEFAULT_SPEC["riscv_qemu_net_num"]
    disk = 0
    qemu_num = server_count  # Pool model: server_count equals QEMU count

    # Take max requirements from FMF inheritance chain
    for fmf in all_fmf_files:
        hw = parse_hardware_require([fmf])
        cpu = max(cpu, parse_num(hw.get("cpu"), DEFAULT_SPEC["riscv_qemu_cpu"]))
        memory = max(memory, parse_num(hw.get("memory"), DEFAULT_SPEC["riscv_qemu_memory"]))
        net = max(net, parse_num(hw.get("net"), DEFAULT_SPEC["riscv_qemu_net_num"]))
        disk = max(disk, parse_num(hw.get("disk"), 0))

    # Extended rule bonuses (take max)
    for rule in matched_rules:
        cpu = max(cpu, rule["cpu"])
        memory = max(memory, rule["memory"])
        qemu_num = max(qemu_num, rule["qemu_num"])
        disk = max(disk, rule["disk"])
        net = max(net, rule["net"])

    # Data disks: 20G each
    disk_sizes = [20] * disk if disk > 0 else []

    # QEMU count tiering (split into multiple QEMU instances when many test cases)
    total_items = len(test_paths) + len(suite_paths)
    for threshold, num in QEMU_NUM_TIERS:
        if total_items > threshold:
            qemu_num = max(qemu_num, num)

    # SKU selection (ensure it can carry cpu*qemu_num / memory*qemu_num)
    sku = pick_sku(cpu * qemu_num, memory * qemu_num)

    reason_parts = [f"{total_items} test directories"]
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
        "server_count": server_count,
        "packages": sorted(all_pkgs),
        "reason": "; ".join(reason_parts),
    }
    return test_paths, suite_paths, spec


class ComputeRequirementsCommand(BaseCommand):
    """Compute CloudPods QEMU VM resource spec based on tests/ changed files"""

    name = "compute-requirements"
    description = "Compute VM resource spec (QEMU count/CPU/memory/NICs/disk) based on tests/ changed files"

    def setup_parser(self, parser):
        parser.add_argument("--repo", required=True, help="Repository root path")
        parser.add_argument("--changed-files", required=True,
                            help="File listing changed files under tests/")
        parser.add_argument("--output", required=True, help="Output JSON path")

    def run(self, args) -> int:
        repo_root = Path(args.repo).resolve()
        with open(args.changed_files, encoding="utf-8") as f:
            changed_files = [ln.strip() for ln in f if ln.strip()]

        if not changed_files:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump({"test_paths": [], "suite_paths": [], "spec": {}},
                          f, ensure_ascii=False, indent=2)
            self.log_info("No changed files")
            return 0

        test_paths, suite_paths, spec = compute_spec(changed_files, repo_root)

        result = {"test_paths": test_paths, "suite_paths": suite_paths, "spec": spec}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        self.log_info(f"test_paths: {test_paths}")
        self.log_info(f"suite_paths: {suite_paths}")
        self.log_info(f"spec: {json.dumps(spec, ensure_ascii=False)}")
        return 0
