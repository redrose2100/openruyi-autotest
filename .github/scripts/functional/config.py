# -*- coding: utf-8 -*-
"""Functional test configuration file loading and merging.

The config file is at .github/scripts/functional/config.json, used as defaults;
environment variables can override key items (for CI injection):
  FUNC_TEST_CONCURRENCY     Number of concurrent test suites
  FUNC_TEST_ENV_PREFIX      Environment naming prefix
  FUNC_TEST_REPORTS_ROOT    Report output root directory
  CLOUDPODS_KEYSTONE_URL    Credentials (via existing env)
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
    """Load default config, overlay with environment variables and explicit caller overrides."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg: Dict[str, Any] = json.load(f)
    else:
        cfg = {}

    # Environment variable overrides
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
    """Get the environment spec for a test suite (default spec + per-suite override)."""
    spec = dict(cfg.get("default_spec", {}))
    suites_cfg = cfg.get("suites", {})
    if suite_name in suites_cfg and isinstance(suites_cfg[suite_name], dict):
        spec.update(suites_cfg[suite_name].get("spec", {}))
    return spec
