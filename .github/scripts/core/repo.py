# -*- coding: utf-8 -*-
"""
仓库根目录查找与打包工具。

关键点：runner 的 checkout 目录是
  /home/github-runner/actions-runner/_work/<repo>/<repo>/
（仓库根 = .github 的上一级），因此向上查找 .git 目录。
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
    """向上查找包含 .git 的目录作为仓库根。"""
    start = start or Path(__file__).resolve().parent.parent
    for p in [start, *start.parents]:
        if (p / ".git").exists() or (p / ".git").is_file():
            return p
    # 兜底：.github/scripts/ 上溯三级
    return start.parents[2] if len(start.parents) >= 3 else start


def get_changed_files(base_sha: str, head_sha: str, path_filter: str = "") -> List[str]:
    """获取 base..head 之间改动的文件（可用 path_filter 限定，如 tests/）。"""
    cmd = ["git", "diff", "--name-only", base_sha, head_sha]
    if path_filter:
        cmd += ["--", path_filter]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(find_repo_root()))
    if result.returncode != 0:
        return []
    return [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]


def package_repo(repo_root: Path, excludes: Optional[List[str]] = None) -> str:
    """把仓库打包为 tar.gz（排除 .git 与无关大目录），返回临时文件路径。"""
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
    """确保仓库根在 sys.path，以便 import tools/cloudpods 等模块。"""
    root = module_root or find_repo_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)
