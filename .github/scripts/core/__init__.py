# -*- coding: utf-8 -*-
"""
core 包：CI CLI 公共基础设施。

分层设计：
  base       — BaseCommand 基类 + CommandRegistry 自动注册器
  logging    — 统一日志组件（控制台/文件/JSON）
  config     — 环境变量与 JSON 读写工具
  repo       — 仓库根目录查找、打包、改动文件收集
  ssh        — 统一 SSH 客户端（ExecResult + 脚本执行 + 等待就绪）
  github     — GitHub REST API 封装
  cloudpods  — CloudPods 云平台 API 客户端（create_server 的轻量封装）

命令（commands/）只依赖 core 基础设施，彼此不互相 import，保持解耦。
"""
