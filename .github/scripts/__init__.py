# -*- coding: utf-8 -*-
"""
openruyi-autotest CI CLI 包。

统一入口: python3 .github/scripts/cli.py <command> [args...]
所有 CI 检查/操作为基于 BaseCommand 的子命令，位于 commands/ 目录，
通过 CommandRegistry 自动发现并注册。
"""
