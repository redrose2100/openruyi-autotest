# -*- coding: utf-8 -*-
"""
Repo root directory discovery and packaging utilities.

Key point: the runner checkout directory is
  /home/github-runner/actions-runner/_work/<repo>/<repo>/
(repo root = parent of .github), so search upward for the .git directory.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import List, Optional


def find_repo_root(start: Optional[Path] = None) -> Path:
    """Walk upward to find the directory containing .git as the repo root."""
    start = start or Path(__file__).resolve().parent.parent
    for p in [start, *start.parents]:
        if (p / ".git").exists() or (p / ".git").is_file():
            return p
    # Fallback: go up 3 levels from .github/scripts/
    return start.parents[2] if len(start.parents) >= 3 else start


def get_changed_files(base_sha: str, head_sha: str, path_filter: str = "") -> List[str]:
    """Get files changed between base..head (optionally filter by path, e.g. tests/)."""
    cmd = ["git", "diff", "--name-only", base_sha, head_sha]
    if path_filter:
        cmd += ["--", path_filter]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(find_repo_root()))
    if result.returncode != 0:
        return []
    return [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]


def package_repo(repo_root: Path, excludes: Optional[List[str]] = None) -> str:
    """Package the repo as tar.gz (excluding .git and irrelevant directories), return temp file path."""
    excludes = excludes or [".git", "docs", ".github", "unittests"]
    fd, tmp = tempfile.mkstemp(suffix=".tar.gz")
    os.close(fd)

    with tarfile.open(tmp, "w:gz") as tar:
        for child in sorted(repo_root.iterdir()):
            if child.name in excludes:
                continue
            tar.add(child, arcname=f"openruyi-autotest/{child.name}")
    return tmp


def ensure_on_path(module_root: Optional[Path] = None) -> None:
    """Ensure the repo root is on sys.path so modules like tools/cloudpods can be imported."""
    root = module_root or find_repo_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)
