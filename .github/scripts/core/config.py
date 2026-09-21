# -*- coding: utf-8 -*-
"""
Configuration and environment variable utilities.

Design highlights:
  * In CI scenarios, most config is injected via environment variables (e.g. GITHUB_TOKEN, CLOUDPODS_*).
  * Provides unified env reading / type conversion (int/bool/list/json), avoiding per-command parsing duplication.
  * Provides JSON file read/write (commands pass intermediate results via JSON files, decoupled and auditable).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Environment variable reading
# ---------------------------------------------------------------------------
def get_env(name: str, default: str = "") -> str:
    """Read an environment variable, returning default if absent."""
    val = os.environ.get(name)
    return val if val is not None else default


def get_env_int(name: str, default: int = 0) -> int:
    """Read an environment variable and convert to int; return default on invalid/missing."""
    val = os.environ.get(name)
    if val is None or val.strip() == "":
        return default
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def get_env_bool(name: str, default: bool = False) -> bool:
    """Read an environment variable and convert to bool ('1'/'true'/'yes'/'on' -> True)."""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def get_env_list(name: str, default: Optional[List[str]] = None) -> List[str]:
    """Read a comma-separated environment variable as a list."""
    val = os.environ.get(name)
    if not val:
        return list(default) if default else []
    return [x.strip() for x in val.split(",") if x.strip()]


def get_env_json(name: str, default: Any = None) -> Any:
    """Read a JSON-formatted environment variable (e.g. '{"a":1}' or '[1,2]')."""
    val = os.environ.get(name)
    if not val:
        return default
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return default


# ---------------------------------------------------------------------------
# JSON file read/write
# ---------------------------------------------------------------------------
def read_json(path: Path, default: Any = None) -> Any:
    """Read a JSON file, returning default on failure."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    """Write a JSON file (auto-creates parent directories)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


# ---------------------------------------------------------------------------
# GitHub Actions output
# ---------------------------------------------------------------------------
def set_github_output(name: str, value: Any) -> None:
    """Write to GitHub Actions $GITHUB_OUTPUT (when running in CI)."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def set_github_env(name: str, value: Any) -> None:
    """Write to GitHub Actions $GITHUB_ENV (when running in CI)."""
    env_file = os.environ.get("GITHUB_ENV")
    if not env_file:
        return
    with open(env_file, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def github_context() -> Dict[str, str]:
    """Collect common GitHub Actions context (repo / PR / SHA)."""
    return {
        "repository": get_env("GITHUB_REPOSITORY"),
        "pr_number": get_env("PR_NUMBER"),
        "token": get_env("GITHUB_TOKEN"),
        "workspace": get_env("GITHUB_WORKSPACE"),
        "head_sha": get_env("GITHUB_SHA"),
    }
