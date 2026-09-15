#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openruyi-autotest CI 命令行统一入口。

用法：
  python3 .github/scripts/cli.py <command> [args...]

命令自动发现于 commands/ 目录（每个命令一个文件，继承 BaseCommand）。
运行 `python3 .github/scripts/cli.py --help` 查看所有命令。
"""
from __future__ import annotations

import sys
from pathlib import Path

# 保证 cli.py 直接执行时能以绝对包名 import core/commands
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.base import run_cli  # noqa: E402


def main() -> int:
    return run_cli(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
