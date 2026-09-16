# -*- coding: utf-8 -*-
"""
命令基类与注册机制。

设计要点：
  * 每个 CI 命令是一个继承 BaseCommand 的类，放在 commands/ 目录下一个文件一个命令。
  * CommandRegistry 通过包内文件自动发现命令类并注册，无需手工维护命令列表。
  * 命令之间通过共享的 core 基础组件（SSH、GitHub API、日志等）协作，彼此解耦。
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type

# scripts 目录（core/base.py 的上级）
SCRIPTS_DIR = Path(__file__).resolve().parent.parent

# 保证 `python3 cli.py` / `python3 -m scripts` 都能以绝对包名 import
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from core.logging import setup_logging  # noqa: E402

logger = logging.getLogger("ci_cli")


class BaseCommand:
    """所有 CI 子命令的基类。

    子类需要定义:
      name        — 命令行名称（默认取类名的 snake_case）
      description — 帮助信息

    并实现:
      setup_parser(parser)  — 添加自定义参数（可选）
      run(args)             — 命令主逻辑，返回 0 成功 / 非 0 失败
    """

    #: 命令名；不指定时由类名自动推导（CamelCase -> snake_case）
    name: Optional[str] = None
    #: 一行帮助说明
    description: str = ""
    #: 命令执行超时（秒），None 表示不限制
    timeout: Optional[int] = None

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """子类可在此添加自己的参数。"""

    def run(self, args: argparse.Namespace) -> int:
        """命令主逻辑。返回 0 表示成功。"""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # 生命周期钩子
    # ------------------------------------------------------------------
    def on_start(self, args: argparse.Namespace) -> None:
        """run 之前调用，可用于初始化。"""

    def on_finish(self, args: argparse.Namespace, exit_code: int) -> None:
        """run 之后调用，可用于清理。"""

    # ------------------------------------------------------------------
    # 工具方法
    # ------------------------------------------------------------------
    @property
    def repo_root(self) -> Path:
        """仓库根目录（.github 的上一级，即 .git 所在目录）。"""
        from core.repo import find_repo_root

        return find_repo_root()

    @property
    def scripts_dir(self) -> Path:
        """scripts 目录。"""
        return SCRIPTS_DIR

    @property
    def github_dir(self) -> Path:
        """.github 目录。"""
        return SCRIPTS_DIR.parent

    def log_info(self, msg: str, *args: object) -> None:
        logger.info(msg, *args)

    def log_warn(self, msg: str, *args: object) -> None:
        logger.warning(msg, *args)

    def log_error(self, msg: str, *args: object) -> None:
        logger.error(msg, *args)

    def log_debug(self, msg: str) -> None:
        logger.debug(msg)

    @classmethod
    def camel_to_snake(cls, name: str) -> str:
        """CamelCase -> snake_case，用于自动推导命令名。"""
        import re

        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _iter_command_modules() -> List[str]:
    """列出 commands/ 目录下所有 .py 模块名（跳过 _ 开头）。"""
    commands_dir = SCRIPTS_DIR / "commands"
    if not commands_dir.is_dir():
        return []
    return sorted(p.stem for p in commands_dir.glob("*.py") if not p.name.startswith("_"))


class CommandRegistry:
    """命令注册表：自动发现 commands/ 目录中的命令类。"""

    def __init__(self) -> None:
        self._commands: Dict[str, Type[BaseCommand]] = {}

    # ------------------------------------------------------------------
    # 发现与注册
    # ------------------------------------------------------------------
    def discover(self) -> None:
        """扫描 commands/ 目录，自动注册所有 BaseCommand 子类。"""
        for module_name in _iter_command_modules():
            try:
                module = importlib.import_module(f"commands.{module_name}")
            except Exception as exc:  # noqa: BLE001 - 单个命令失败不应拖垮整个 CLI
                logger.error("加载命令模块 %s 失败: %s", module_name, exc)
                continue

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, BaseCommand)
                    and obj is not BaseCommand
                    and getattr(obj, "__module__", "") == module.__name__
                ):
                    self.register(obj)

    def register(self, cmd_cls: Type[BaseCommand]) -> None:
        """注册一个命令类（显式或自动调用）。"""
        name = cmd_cls.name or BaseCommand.camel_to_snake(cmd_cls.__name__)
        if name in self._commands:
            logger.warning("命令 %s 重复注册，覆盖", name)
        self._commands[name] = cmd_cls

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------
    @property
    def commands(self) -> Dict[str, Type[BaseCommand]]:
        return self._commands

    def get(self, name: str) -> Optional[Type[BaseCommand]]:
        return self._commands.get(name)

    def names(self) -> List[str]:
        return sorted(self._commands.keys())

    # ------------------------------------------------------------------
    # 构建 argparse 顶层解析器
    # ------------------------------------------------------------------
    def build_parser(self, prog: Optional[str] = None) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog=prog or "ci-cli",
            description="openruyi-autotest CI 命令集合",
        )
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="提高日志级别（-v INFO, -vv DEBUG）",
        )
        parser.add_argument(
            "--log-file", default=None,
            help="同时将日志写入该文件（文件始终记录到 DEBUG）",
        )
        sub = parser.add_subparsers(dest="command", metavar="<command>", required=True)

        for name in self.names():
            cmd_cls = self._commands[name]
            sub_parser = sub.add_parser(name, help=cmd_cls.description)
            sub_parser.set_defaults(_cmd_cls=cmd_cls)
            # 实例化（不执行）以调用 setup_parser
            cmd_cls().setup_parser(sub_parser)

        return parser

    # ------------------------------------------------------------------
    # 执行入口
    # ------------------------------------------------------------------
    def main(self, argv: Optional[List[str]] = None) -> int:
        """注册所有命令、解析参数并执行。返回进程退出码。"""
        self.discover()
        if not self._commands:
            logger.error("未发现任何命令，请检查 commands/ 目录")
            return 2

        parser = self.build_parser()
        args = parser.parse_args(argv)

        # 日志级别（统一走 core.logging.setup_logging）
        level = logging.WARNING
        if args.verbose >= 2:
            level = logging.DEBUG
        elif args.verbose == 1:
            level = logging.INFO
        setup_logging(level=level, log_file=getattr(args, "log_file", None))

        cmd_cls = args._cmd_cls
        cmd = cmd_cls()
        exit_code = 0
        try:
            cmd.on_start(args)
            exit_code = cmd.run(args) or 0
        except KeyboardInterrupt:
            logger.error("命令被中断")
            exit_code = 130
        except Exception as exc:  # noqa: BLE001
            logger.error("命令 %s 执行失败: %s", cmd_cls.name or cmd_cls.__name__, exc)
            if args.verbose >= 2:
                logger.debug("traceback:", exc_info=True)
            exit_code = 1
        finally:
            try:
                cmd.on_finish(args, exit_code)
            except Exception:  # noqa: BLE001
                logger.exception("on_finish 回调失败")
        return exit_code


def run_cli(argv: Optional[List[str]] = None) -> int:
    """供 `python3 -m scripts` 或 cli.py 调用的便捷入口。"""
    registry = CommandRegistry()
    return registry.main(argv)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(run_cli())
