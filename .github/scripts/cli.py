#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openruyi-autotest CI CLI unified entry point.

Usage:
  python3 .github/scripts/cli.py <command> [args...]

Commands are auto-discovered from the commands/ directory (one file per
command, inheriting BaseCommand). Run `python3 .github/scripts/cli.py --help`
to list all commands.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure cli.py can import core/commands with absolute package names when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.base import run_cli  # noqa: E402


def main() -> int:
    return run_cli(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
