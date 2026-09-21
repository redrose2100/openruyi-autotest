# -*- coding: utf-8 -*-
"""
core package: CI CLI shared infrastructure.

Layered design:
  base       — BaseCommand base class + CommandRegistry auto-registration
  logging    — Unified logging component (console/file/JSON)
  config     — Environment variable and JSON read/write utilities
  repo       — Repo root detection, packaging, changed file collection
  ssh        — Unified SSH client (ExecResult + script execution + wait-for-ready)
  github     — GitHub REST API wrapper
  cloudpods  — CloudPods cloud platform API client (lightweight wrapper around create_server)

Commands (commands/) only depend on core infrastructure, never import each other, staying decoupled.
"""
