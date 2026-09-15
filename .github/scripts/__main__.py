# -*- coding: utf-8 -*-
"""
支持 `python3 -m scripts <command>` 方式调用（从仓库根目录）。
"""
from __future__ import annotations

import sys

from core.base import run_cli

if __name__ == "__main__":
    sys.exit(run_cli())
