# -*- coding: utf-8 -*-
"""
Command base class and registration mechanism.

Design highlights:
  * Each CI command is a class inheriting BaseCommand, one command per file under commands/.
  * CommandRegistry auto-discovers and registers command classes from package files;
    no manual maintenance of the command list required.
  * Commands collaborate through shared core components (SSH, GitHub API, logging, etc.)
    while remaining decoupled from each other.
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type

# scripts directory (parent of core/base.py)
SCRIPTS_DIR = Path(__file__).resolve().parent.parent

# Ensure both `python3 cli.py` and `python3 -m scripts` can import using absolute package names
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from core.logging import setup_logging  # noqa: E402

logger = logging.getLogger("ci_cli")


class BaseCommand:
    """Base class for all CI sub-commands.

    Subclasses should define:
      name        — CLI name (defaults to snake_case of class name)
      description — Help text

    and implement:
      setup_parser(parser)  — Add custom arguments (optional)
      run(args)             — Main command logic, returns 0 for success / non-zero for failure
    """

    #: Command name; auto-derived from class name if not specified (CamelCase -> snake_case)
    name: Optional[str] = None
    #: One-line help description
    description: str = ""
    #: Command execution timeout (seconds); None means unlimited
    timeout: Optional[int] = None

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """Subclass can add its own arguments here."""

    def run(self, args: argparse.Namespace) -> int:
        """Main command logic. Return 0 for success."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Lifecycle hooks
    # ------------------------------------------------------------------
    def on_start(self, args: argparse.Namespace) -> None:
        """Called before run, for initialization."""

    def on_finish(self, args: argparse.Namespace, exit_code: int) -> None:
        """Called after run, for cleanup."""

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    @property
    def repo_root(self) -> Path:
        """Repo root directory (parent of .github, i.e. the directory containing .git)."""
        from core.repo import find_repo_root

        return find_repo_root()

    @property
    def scripts_dir(self) -> Path:
        """scripts directory."""
        return SCRIPTS_DIR

    @property
    def github_dir(self) -> Path:
        """.github directory."""
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
        """CamelCase -> snake_case, for auto-deriving command names."""
        import re

        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _iter_command_modules() -> List[str]:
    """List all .py module names under commands/ (skip names starting with _)."""
    commands_dir = SCRIPTS_DIR / "commands"
    if not commands_dir.is_dir():
        return []
    return sorted(p.stem for p in commands_dir.glob("*.py") if not p.name.startswith("_"))


class CommandRegistry:
    """Command registry: auto-discovers command classes from the commands/ directory."""

    def __init__(self) -> None:
        self._commands: Dict[str, Type[BaseCommand]] = {}

    # ------------------------------------------------------------------
    # Discovery and registration
    # ------------------------------------------------------------------
    def discover(self) -> None:
        """Scan commands/ directory, auto-register all BaseCommand subclasses."""
        for module_name in _iter_command_modules():
            try:
                module = importlib.import_module(f"commands.{module_name}")
            except Exception as exc:  # noqa: BLE001 - a single command failure should not bring down the whole CLI
                logger.error("Failed to load command module %s: %s", module_name, exc)
                continue

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, BaseCommand)
                    and obj is not BaseCommand
                    and getattr(obj, "__module__", "") == module.__name__
                ):
                    self.register(obj)

    def register(self, cmd_cls: Type[BaseCommand]) -> None:
        """Register a command class (called explicitly or automatically)."""
        name = cmd_cls.name or BaseCommand.camel_to_snake(cmd_cls.__name__)
        if name in self._commands:
            logger.warning("Command %s registered twice, overwriting", name)
        self._commands[name] = cmd_cls

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------
    @property
    def commands(self) -> Dict[str, Type[BaseCommand]]:
        return self._commands

    def get(self, name: str) -> Optional[Type[BaseCommand]]:
        return self._commands.get(name)

    def names(self) -> List[str]:
        return sorted(self._commands.keys())

    # ------------------------------------------------------------------
    # Build argparse top-level parser
    # ------------------------------------------------------------------
    def build_parser(self, prog: Optional[str] = None) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog=prog or "ci-cli",
            description="openruyi-autotest CI command collection",
        )
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="Increase log level (-v INFO, -vv DEBUG)",
        )
        parser.add_argument(
            "--log-file", default=None,
            help="Also write logs to this file (file always records at DEBUG)",
        )
        sub = parser.add_subparsers(dest="command", metavar="<command>", required=True)

        for name in self.names():
            cmd_cls = self._commands[name]
            sub_parser = sub.add_parser(name, help=cmd_cls.description)
            sub_parser.set_defaults(_cmd_cls=cmd_cls)
            # Instantiate (without executing) to call setup_parser
            cmd_cls().setup_parser(sub_parser)

        return parser

    # ------------------------------------------------------------------
    # Execution entry point
    # ------------------------------------------------------------------
    def main(self, argv: Optional[List[str]] = None) -> int:
        """Register all commands, parse arguments, and execute. Returns process exit code."""
        self.discover()
        if not self._commands:
            logger.error("No commands discovered, check commands/ directory")
            return 2

        parser = self.build_parser()
        args = parser.parse_args(argv)

        # Log level (unified via core.logging.setup_logging)
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
            logger.error("Command interrupted")
            exit_code = 130
        except Exception as exc:  # noqa: BLE001
            logger.error("Command %s execution failed: %s", cmd_cls.name or cmd_cls.__name__, exc)
            if args.verbose >= 2:
                logger.debug("traceback:", exc_info=True)
            exit_code = 1
        finally:
            try:
                cmd.on_finish(args, exit_code)
            except Exception:  # noqa: BLE001
                logger.exception("on_finish callback failed")
        return exit_code


def run_cli(argv: Optional[List[str]] = None) -> int:
    """Convenience entry point for `python3 -m scripts` or cli.py."""
    registry = CommandRegistry()
    return registry.main(argv)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(run_cli())
