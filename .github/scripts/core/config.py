# -*- coding: utf-8 -*-
"""
配置与环境变量工具。

设计要点：
  * CI 场景中大量配置通过环境变量注入（如 GITHUB_TOKEN、CLOUDPODS_*）。
  * 提供统一的 env 读取/类型转换（int/bool/list/json），避免各命令重复解析。
  * 提供 JSON 文件读写（命令间通过 JSON 文件传递中间结果，解耦且可审计）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# 环境变量读取
# ---------------------------------------------------------------------------
def get_env(name: str, default: str = "") -> str:
    """读取环境变量，缺省返回 default。"""
    val = os.environ.get(name)
    return val if val is not None else default


def get_env_int(name: str, default: int = 0) -> int:
    """读取环境变量并转为 int，非法或缺省返回 default。"""
    val = os.environ.get(name)
    if val is None or val.strip() == "":
        return default
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def get_env_bool(name: str, default: bool = False) -> bool:
    """读取环境变量并转为 bool（'1'/'true'/'yes'/'on' 为 True）。"""
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def get_env_list(name: str, default: Optional[List[str]] = None) -> List[str]:
    """读取逗号分隔的环境变量为列表。"""
    val = os.environ.get(name)
    if not val:
        return list(default) if default else []
    return [x.strip() for x in val.split(",") if x.strip()]


def get_env_json(name: str, default: Any = None) -> Any:
    """读取 JSON 形式的环境变量（如 '{"a":1}' 或 '[1,2]'）。"""
    val = os.environ.get(name)
    if not val:
        return default
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return default


# ---------------------------------------------------------------------------
# JSON 文件读写
# ---------------------------------------------------------------------------
def read_json(path: Path, default: Any = None) -> Any:
    """读取 JSON 文件，失败返回 default。"""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    """写入 JSON 文件（自动创建父目录）。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


# ---------------------------------------------------------------------------
# GitHub Actions 输出
# ---------------------------------------------------------------------------
def set_github_output(name: str, value: Any) -> None:
    """写入 GitHub Actions 的 $GITHUB_OUTPUT（若在 CI 中）。"""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def set_github_env(name: str, value: Any) -> None:
    """写入 GitHub Actions 的 $GITHUB_ENV（若在 CI 中）。"""
    env_file = os.environ.get("GITHUB_ENV")
    if not env_file:
        return
    with open(env_file, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def github_context() -> Dict[str, str]:
    """收集 GitHub Actions 常用上下文（repo / pr / sha）。"""
    return {
        "repository": get_env("GITHUB_REPOSITORY"),
        "pr_number": get_env("PR_NUMBER"),
        "token": get_env("GITHUB_TOKEN"),
        "workspace": get_env("GITHUB_WORKSPACE"),
        "head_sha": get_env("GITHUB_SHA"),
    }
