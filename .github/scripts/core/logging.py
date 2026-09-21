# -*- coding: utf-8 -*-
"""
Unified logging component.

Design highlights:
  * All commands use get_logger() to obtain a logger, avoiding duplicate output from
    individually created handlers.
  * The CLI entry point (core.base.CommandRegistry.main) calls setup_logging() to
    configure root logging; command modules use logging.getLogger("ci.<command>")
    without needing their own configuration.
  * Supports file logging (--log-file) and structured logging (--log-format json)
    for CI-side collection.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from typing import Optional

# Logger name used by the create_server.py copy (it uses logging.getLogger("create_server") internally)
CREATE_SERVER_LOGGER = "create_server"
CLI_LOGGER = "ci_cli"

_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def parse_level(name: str) -> int:
    """Convert 'DEBUG'/'INFO'/'WARNING'/'ERROR' strings to logging levels."""
    return _LEVELS.get(str(name).upper(), logging.INFO)


class JsonFormatter(logging.Formatter):
    """JSON log formatter: each log entry is output as one line of JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "text",
    quiet: bool = False,
) -> None:
    """Configure root logging (idempotent: subsequent calls first clean up existing handlers).

    Parameters:
      level      — Log level name (DEBUG/INFO/WARNING/ERROR)
      log_file   — If specified, also output to this file
      log_format — 'text' or 'json'
      quiet      — If True, suppress console output (file only)
    """
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.setLevel(parse_level(level))

    formatter = JsonFormatter() if log_format == "json" else logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not quiet:
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        root.addHandler(console)

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get the unified logger (recommended for use inside commands)."""
    return logging.getLogger(name)
