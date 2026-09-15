# -*- coding: utf-8 -*-
"""
统一日志组件。

设计要点：
  * 所有命令统一使用 get_logger() 获取 logger，避免各自创建 handler 导致重复输出。
  * CLI 入口（core.base.CommandRegistry.main）统一调用 setup_logging() 配置根日志；
    命令模块内使用 logging.getLogger("ci.<command>")，无需自行配置。
  * 支持文件日志（--log-file）与结构化日志（--log-format json），供 CI 侧收集。
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from typing import Optional

# 供 create_server.py 复制版使用的 logger 名（其内部使用 logging.getLogger("create_server")）
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
    """把 'DEBUG'/'INFO'/'WARNING'/'ERROR' 字符串转为 logging 级别。"""
    return _LEVELS.get(str(name).upper(), logging.INFO)


class JsonFormatter(logging.Formatter):
    """JSON 日志格式器：每条日志输出为一行 JSON。"""

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
    """配置根日志（幂等：多次调用会先清理已存在的 handlers）。

    参数：
      level      — 日志级别名称（DEBUG/INFO/WARNING/ERROR）
      log_file   — 若指定，同时输出到该文件
      log_format — 'text' 或 'json'
      quiet      — 若为 True，则不在控制台输出（仅文件）
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
    """获取统一 logger（推荐命令内使用）。"""
    return logging.getLogger(name)
