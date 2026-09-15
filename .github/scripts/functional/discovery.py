# -*- coding: utf-8 -*-
"""functional 测试套/用例发现。

扫描 tests/functional/pkgs/ 下每个测试套目录：
  - 测试套 = 直接子目录（含 main.fmf）
  - 用例 = 套目录下的 test_* 子目录（含 main.fmf + test.sh）

同时从套目录 main.fmf 继承链解析：
  - 资源规格（extra-hardware-require / require 包）
  - 功能点数量（统计 rlRun / rlAssertGrep 调用）
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SUITE_ROOT = "tests/functional/pkgs"
PLANS_ROOT = "plans"


# ------------------------------------------------------------
# fmf 元数据解析（轻量，兼容 compute_requirements 的解析方式）
# ------------------------------------------------------------
def find_fmf_ancestors(test_dir: Path) -> List[Path]:
    """向上查找包含 main.fmf 的目录链（从最近的测试目录到 tests/ 根）。"""
    ancestors: List[Path] = []
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
    raw = raw.strip()
    raw = re.sub(r"#.*$", "", raw).strip()
    raw = raw.strip('"').strip("'")
    return raw


def parse_hardware_require(fmf_files: List[Path]) -> Dict[str, str]:
    """沿继承链（子 -> 父）解析 extra-hardware-require 各字段，合并返回。"""
    hw: Dict[str, str] = {}
    for fmf in fmf_files:
        try:
            lines = fmf.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
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
    """收集 require 中的包名（排除 /path 形式，即排除依赖用例）。"""
    pkgs: set = set()
    for fmf in fmf_files:
        try:
            lines = fmf.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
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
    """把 '>= 4' / '4' / '8 GiB' 等解析为整数。"""
    if not raw:
        return default
    m = re.search(r"(\d+)", raw)
    return int(m.group(1)) if m else default


# ------------------------------------------------------------
# 功能点统计
# ------------------------------------------------------------
# beakerlib 断言/检查类调用都计为一个功能点
POINT_PATTERNS = [
    re.compile(r"\brlRun\b"),
    re.compile(r"\brlAssertGrep\b"),
    re.compile(r"\brlAssertNotGrep\b"),
    re.compile(r"\brlAssertExists\b"),
    re.compile(r"\brlAssertNotExists\b"),
    re.compile(r"\brlAssertEqual\b"),
    re.compile(r"\brlAssertNotEqual\b"),
    re.compile(r"\brlAssertGreater\b"),
    re.compile(r"\brlAssertTrue\b"),
    re.compile(r"\brlAssertFalse\b"),
    re.compile(r"\brlAssertDiffer\b"),
    re.compile(r"\brlAssertNotDiffer\b"),
]


def count_test_points(script_path: Path) -> int:
    """统计脚本中的功能点数量（rlRun/断言调用次数）。"""
    if not script_path.exists():
        return 0
    try:
        content = script_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith(".") or stripped.startswith("source"):
            continue
        for pat in POINT_PATTERNS:
            if pat.search(line):
                count += 1
                break
    return count


# ------------------------------------------------------------
# 测试套/用例模型
# ------------------------------------------------------------
class FuncCase:
    """一个 functional 测试用例（test_* 子目录）。"""

    def __init__(self, suite_name: str, path: Path, fmf_path: str):
        self.suite_name = suite_name
        self.path = path  # 仓库内相对路径（Path）
        self.fmf_path = fmf_path  # /tests/functional/pkgs/xxx/test_xxx
        self.name = path.name
        self.script = None  # 主脚本（main.fmf test: 或 test.sh）
        self.test_points = 0

    def to_dict(self) -> Dict:
        return {
            "suite": self.suite_name,
            "case": self.name,
            "fmf_path": self.fmf_path,
            "test_points": self.test_points,
        }


class FuncSuite:
    """一个 functional 测试套（pkgs/ 下的包目录）。"""

    def __init__(self, name: str, path: Path, fmf_path: str):
        self.name = name
        self.path = path
        self.fmf_path = fmf_path  # /tests/functional/pkgs/xxx
        self.cases: List[FuncCase] = []
        self.hardware: Dict[str, str] = {}
        self.require_pkgs: List[str] = []
        self.points_total = 0

    def to_dict(self) -> Dict:
        return {
            "suite": self.name,
            "fmf_path": self.fmf_path,
            "case_count": len(self.cases),
            "test_points": self.points_total,
            "require": self.require_pkgs,
            "hardware": self.hardware,
        }


def discover_suites(repo_root: Path, cfg: Dict) -> Tuple[List[FuncSuite], List[str]]:
    """发现所有 functional 测试套。

    返回 (suites, errors)；errors 为发现过程中无法解析的套目录名。
    支持 cfg 中的 suite_include / suite_exclude 过滤（按套名）。
    """
    root = repo_root / SUITE_ROOT
    errors: List[str] = []
    include = cfg.get("suite_include") or []
    exclude = cfg.get("suite_exclude") or []

    if not root.is_dir():
        return [], [f"suite root not found: {root}"]

    suites: List[FuncSuite] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if (child / "main.fmf").exists():
            if include and child.name not in include:
                continue
            if child.name in exclude:
                continue
            try:
                suite = build_suite(child, repo_root)
                suites.append(suite)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{child.name}: {exc}")
    return suites, errors


def build_suite(suite_dir: Path, repo_root: Path) -> FuncSuite:
    """构建单个测试套对象（套本身可带用例子目录）。"""
    # 相对 fmf path：从仓库根计算
    try:
        rel = suite_dir.relative_to(repo_root).as_posix()
        fmf_path = "/" + rel
    except ValueError:
        fmf_path = "/" + suite_dir.as_posix()

    suite = FuncSuite(name=suite_dir.name, path=suite_dir, fmf_path=fmf_path)

    # 解析套级硬件/包需求（含继承链）
    fmf_ancestors = find_fmf_ancestors(suite_dir)
    suite.hardware = parse_hardware_require(fmf_ancestors)
    suite.require_pkgs = parse_require(fmf_ancestors)

    # 发现用例：套目录下的 test_* 子目录
    for child in sorted(suite_dir.iterdir()):
        if not child.is_dir() or not child.name.startswith("test_"):
            continue
        if not (child / "main.fmf").exists():
            continue
        try:
            rel_case = child.relative_to(repo_root).as_posix()
            case = FuncCase(
                suite_name=suite.name,
                path=child,
                fmf_path="/" + rel_case,
            )
            # 主脚本：main.fmf 的 test: 字段，或 test.sh
            script = _resolve_case_script(child)
            case.script = script
            case.test_points = count_test_points(script) if script else 0
            suite.points_total += case.test_points
            suite.cases.append(case)
        except Exception:  # noqa: BLE001
            continue

    return suite


def _resolve_case_script(case_dir: Path):
    """解析用例主脚本路径（main.fmf test: 字段优先，其次 test.sh）。"""
    fmf = case_dir / "main.fmf"
    if fmf.exists():
        try:
            for line in fmf.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.match(r"^\s*test\s*:\s*(.+)$", line)
                if m:
                    script_rel = parse_fmf_value(m.group(1))
                    script = case_dir / script_rel
                    if script.exists():
                        return script
        except OSError:
            pass
    for cand in ("test.sh", "runtest.sh", "test"):
        script = case_dir / cand
        if script.exists():
            return script
    return None
