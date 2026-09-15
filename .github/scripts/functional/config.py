# -*- coding: utf-8 -*-
"""功能测试配置文件加载与合并。

配置文件位于 .github/scripts/functional/config.json，作为默认值；
环境变量可覆盖关键项（便于 CI 中注入）：
  FUNC_TEST_CONCURRENCY     并发测试套数
  FUNC_TEST_ENV_PREFIX      环境命名前缀
  FUNC_TEST_REPORTS_ROOT    报告输出根目录
  CLOUDPODS_KEYSTONE_URL    凭据（走既有 env）
  CLOUDPODS_USER
  CLOUDPODS_PASSWORD
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """加载默认配置，叠加环境变量与调用方显式覆盖。"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg: Dict[str, Any] = json.load(f)
    else:
        cfg = {}

    # 环境变量覆盖
    env_mapping = {
        "FUNC_TEST_CONCURRENCY": "concurrency",
        "FUNC_TEST_ENV_PREFIX": "env_prefix",
        "FUNC_TEST_REPORTS_ROOT": "reports_root",
    }
    for env_key, cfg_key in env_mapping.items():
        val = os.environ.get(env_key)
        if val:
            cfg[cfg_key] = int(val) if cfg_key == "concurrency" else val

    if overrides:
        cfg.update({k: v for k, v in overrides.items() if v is not None})

    return cfg


def get_suite_spec(cfg: Dict[str, Any], suite_name: str) -> Dict[str, Any]:
    """获取某个测试套的环境规格（默认规格 + 按测试套覆盖）。"""
    spec = dict(cfg.get("default_spec", {}))
    suites_cfg = cfg.get("suites", {})
    if suite_name in suites_cfg and isinstance(suites_cfg[suite_name], dict):
        spec.update(suites_cfg[suite_name].get("spec", {}))
    return spec
