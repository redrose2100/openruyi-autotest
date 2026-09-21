# -*- coding: utf-8 -*-
"""
Supports `python3 -m scripts <command>` invocation (from repo root).
"""
from __future__ import annotations

import sys

from core.base import run_cli

if __name__ == "__main__":
    sys.exit(run_cli())
