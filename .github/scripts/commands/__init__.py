# -*- coding: utf-8 -*-
"""
commands package: all CI subcommands.

Each command is a separate file, inheriting core.base.BaseCommand,
auto-discovered and registered by CommandRegistry (no manual list maintenance).

Adding a new command:
  1. Create <command_name>.py in this directory
  2. Define class <CommandName>(BaseCommand)
  3. Implement name/description and run(args)
  4. (Optional) Implement setup_parser(args) to add arguments
"""
