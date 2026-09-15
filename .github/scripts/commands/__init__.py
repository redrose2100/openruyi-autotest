# -*- coding: utf-8 -*-
"""
commands 包：所有 CI 子命令。

每个命令一个文件，继承 core.base.BaseCommand，会被 CommandRegistry
自动发现并注册（无需手工维护命令列表）。

新增命令步骤：
  1. 在本目录新建 <command_name>.py
  2. 定义 class <CommandName>(BaseCommand)
  3. 实现 name/description 与 run(args)
  4. （可选）实现 setup_parser(args) 添加参数
"""
