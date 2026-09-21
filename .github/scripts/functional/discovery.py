# -*- coding: utf-8 -*-
"""Functional test suite/case discovery.

Scans each test suite directory under tests/functional/pkgs/:
  - Test suite = direct subdirectory (containing main.fmf)
  - Test case = test_* subdirectory within a suite (containing main.fmf + test.sh)

Also resolves from the suite directory main.fmf inheritance chain:
  - Resource specs (extra-hardware-require / require packages)
  - Feature point count (by counting rlRun / rlAssertGrep calls)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SUITE_ROOT = "tests/functional/pkgs"
PLANS_ROOT = "plans"


# ------------------------------------------------------------
# fmf metadata parsing (lightweight, compatible with compute_requirements parsing approach)
# ------------------------------------------------------------
def find_fmf_ancestors(test_dir: Path) -> List[Path]:
    """Walk upward to find the main.fmf ancestor chain (from nearest test dir to tests/ root)."""
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
    """Resolve extra-hardware-require fields along the inheritance chain (child -> parent), merge and return."""
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
    """Collect package names from require (exclude /path forms, i.e. exclude dependent cases)."""
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
    """Parse strings like '>= 4' / '4' / '8 GiB' into an integer."""
    if not raw:
        return default
    m = re.search(r"(\d+)", raw)
    return int(m.group(1)) if m else default


# ------------------------------------------------------------
# Feature point counting
# ------------------------------------------------------------
# Every beakerlib assertion/check call counts as one feature point
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
    """Count feature points in a script (number of rlRun/assertion calls)."""
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
# Test suite/case models
# ------------------------------------------------------------
class FuncCase:
    """A functional test case (test_* subdirectory)."""

    def __init__(self, suite_name: str, path: Path, fmf_path: str):
        self.suite_name = suite_name
        self.path = path  # Relative path within repo
        self.fmf_path = fmf_path  # /tests/functional/pkgs/xxx/test_xxx
        self.name = path.name
        self.script = None  # Main script (main.fmf test: or test.sh)
        self.test_points = 0

    def to_dict(self) -> Dict:
        return {
            "suite": self.suite_name,
            "case": self.name,
            "fmf_path": self.fmf_path,
            "test_points": self.test_points,
        }


class FuncSuite:
    """A functional test suite (package directory under pkgs/)."""

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
    """Discover all functional test suites.

    Returns (suites, errors); errors are suite directory names that could not
    be parsed during discovery.
    Supports suite_include / suite_exclude filtering from cfg (by suite name).
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
    """Build a single test suite object (suite can contain test case subdirectories)."""
    # Relative fmf path: compute from repo root
    try:
        rel = suite_dir.relative_to(repo_root).as_posix()
        fmf_path = "/" + rel
    except ValueError:
        fmf_path = "/" + suite_dir.as_posix()

    suite = FuncSuite(name=suite_dir.name, path=suite_dir, fmf_path=fmf_path)

    # Resolve suite-level hardware/package requirements (including inheritance chain)
    fmf_ancestors = find_fmf_ancestors(suite_dir)
    suite.hardware = parse_hardware_require(fmf_ancestors)
    suite.require_pkgs = parse_require(fmf_ancestors)

    # Discover cases: test_* subdirectories within the suite directory
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
            # Main script: main.fmf test: field, or test.sh
            script = _resolve_case_script(child)
            case.script = script
            case.test_points = count_test_points(script) if script else 0
            suite.points_total += case.test_points
            suite.cases.append(case)
        except Exception:  # noqa: BLE001
            continue

    return suite


def _resolve_case_script(case_dir: Path):
    """Resolve the case main script path (main.fmf test: field first, then test.sh)."""
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
