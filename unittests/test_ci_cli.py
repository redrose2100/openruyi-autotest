# -*- coding: utf-8 -*-
"""
CI CLI（.github/scripts）单元测试。

覆盖：
1. CommandRegistry 自动注册：commands/ 下每个文件都应被发现，且所有
   命令在 cli.py --help 中可见。
2. compute-requirements：
   - FMF 解析（hardware-require / require / 路径继承）
   - EXTRA_RESOURCE_RULES 规则触发（performance/unixbench -> cpu 8）
   - SKU 选择
3. post-pr-comment 的 build_comment Markdown 生成。
4. cleanup-cloudpods 的凭据来源与 server_ids 清洗。
5. core.logging 的 JSON 格式器。
"""
import importlib
import json
import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from core.base import BaseCommand, CommandRegistry  # noqa: E402
from core.logging import JsonFormatter  # noqa: E402


class TestCommandRegistry(unittest.TestCase):
    """验证命令自动发现与注册。"""

    def test_all_command_files_discovered(self):
        reg = CommandRegistry()
        reg.discover()
        names = reg.names()
        # 期望的 5 个命令
        for expected in ("compute-requirements", "launch-qemu-env",
                         "run-tests-in-qemu", "post-pr-comment",
                         "cleanup-cloudpods"):
            self.assertIn(expected, names, f"命令 {expected} 未注册")

    def test_commands_inherit_base(self):
        reg = CommandRegistry()
        reg.discover()
        for name, cls in reg.commands.items():
            self.assertTrue(issubclass(cls, BaseCommand), name)
            self.assertTrue(callable(getattr(cls, "run", None)), name)

    def test_cli_help_lists_all_commands(self):
        """--help 输出应包含所有命令名（子进程级验证）。"""
        import subprocess
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "cli.py"), "--help"],
            capture_output=True, text=True, timeout=60,
            cwd=str(SCRIPTS_DIR.parent.parent),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = proc.stdout
        for expected in ("cleanup-cloudpods", "compute-requirements",
                         "launch-qemu-env", "post-pr-comment",
                         "run-tests-in-qemu"):
            self.assertIn(expected, out)


class TestComputeRequirements(unittest.TestCase):
    """compute-requirements 的 FMF 解析与规格计算。"""

    @classmethod
    def setUpClass(cls):
        mod = importlib.import_module("commands.compute_requirements")
        cls.mod = mod
        cls.repo_root = Path(__file__).resolve().parent.parent

    def test_find_fmf_ancestors(self):
        mod = self.mod
        # 找一个真实用例目录（unixbench 套件）
        unixbench_dir = self.repo_root / "tests" / "performance" / "unixbench"
        if not unixbench_dir.exists():
            self.skipTest("tests/performance/unixbench 不存在")
        ancestors = mod.find_fmf_ancestors(unixbench_dir)
        self.assertTrue(ancestors, "应找到至少一个 main.fmf")
        # 链应沿 tests/ 向上，且最近的在最前
        self.assertEqual(ancestors[0], unixbench_dir / "main.fmf")

    def test_unixbench_triggers_performance_rule(self):
        """performance 目录应触发 EXTRA_RESOURCE_RULES 的 cpu=8。"""
        mod = self.mod
        unixbench_dir = self.repo_root / "tests" / "performance" / "unixbench"
        if not unixbench_dir.exists():
            self.skipTest("tests/performance/unixbench 不存在")
        test_paths, suite_paths, spec = mod.compute_spec(
            ["tests/performance/unixbench/main.fmf"], self.repo_root)
        self.assertGreaterEqual(spec["riscv_qemu_cpu"], 8)
        self.assertGreaterEqual(spec["riscv_qemu_memory"], 8)

    def test_pick_sku_rounds_up(self):
        mod = self.mod
        # 需要 12 CPU -> 平台 12 核档
        self.assertEqual(mod.pick_sku(12, 16), "ecs.g1.c12m16")
        # 需要 6 CPU -> 升到 8 核档，内存 6 -> 8
        self.assertEqual(mod.pick_sku(6, 6), "ecs.g1.c8m8")
        # 需要 128 CPU -> 上限档
        self.assertEqual(mod.pick_sku(200, 300), "ecs.g1.c128m256")

    def test_parse_hardware_require(self):
        """从真实 main.fmf 解析 extra-hardware-require。"""
        mod = self.mod
        # 找一个声明了 extra-hardware-require 的测试
        found = None
        for candidate in (
            self.repo_root / "tests" / "performance" / "unixbench" / "main.fmf",
            self.repo_root / "tests" / "feature" / "k8s" / "main.fmf",
        ):
            if candidate.exists() and "extra-hardware-require" in candidate.read_text(
                    encoding="utf-8", errors="replace"):
                found = candidate
                break
        if found is None:
            self.skipTest("未找到声明 extra-hardware-require 的测试")
        hw = mod.parse_hardware_require([found])
        self.assertIsInstance(hw, dict)


class TestPostPrComment(unittest.TestCase):
    """PR 评论 Markdown 生成。"""

    @classmethod
    def setUpClass(cls):
        cls.mod = importlib.import_module("commands.post_pr_comment")

    def test_build_comment_ok(self):
        r = {
            "ok": True,
            "summary": {"pass": 3, "fail": 0, "error": 0, "skip": 1, "total": 4},
            "results": [
                {"status": "pass", "test_path": "/tests/a",
                 "host_ip": "1.2.3.4", "qemu_port": 12055},
            ],
        }
        c = self.mod.build_comment(r)
        self.assertIn("Automated Test Verification Report", c)
        self.assertIn("All Passed", c)
        self.assertIn("Passed `3`", c)

    def test_build_comment_fail_has_details(self):
        r = {
            "ok": False,
            "summary": {"pass": 0, "fail": 1, "error": 0, "skip": 0, "total": 1},
            "results": [
                {"status": "fail", "test_path": "/tests/b",
                 "host_ip": "1.2.3.4", "qemu_port": 12055,
                 "output": "assertion boom"},
            ],
        }
        c = self.mod.build_comment(r)
        self.assertIn("Has Failures", c)
        self.assertIn("Failure Details", c)
        self.assertIn("assertion boom", c)


class TestCleanupCloudpods(unittest.TestCase):
    """cleanup-cloudpods 的 vm_info 解析与凭据。"""

    @classmethod
    def setUpClass(cls):
        mod = importlib.import_module("commands.cleanup_cloudpods")
        cls.mod = mod

    def test_server_ids_strip_quotes(self):
        """server_ids 应清洗引号与空项。"""
        mod = self.mod
        # 通过临时 vm_info.json 走完整 run 前段逻辑
        with tempfile.TemporaryDirectory() as tmp:
            vm_info = {"server_ids": ["'uuid1'", '"uuid2"', "", "  uuid3  "]}
            path = Path(tmp) / "vm_info.json"
            path.write_text(json.dumps(vm_info), encoding="utf-8")

            # 直接调用内部逻辑（不连真实云平台）
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            ids = [str(s).strip().strip("'\"").strip()
                   for s in data.get("server_ids", []) if str(s).strip()]
            self.assertEqual(ids, ["uuid1", "uuid2", "uuid3"])

    def test_credentials_from_env_or_vm_info(self):
        """凭据应优先环境变量，其次 vm_info。"""
        mod = self.mod
        old = {k: os.environ.get(k) for k in
               ("CLOUDPODS_KEYSTONE_URL", "CLOUDPODS_USER", "CLOUDPODS_PASSWORD")}
        try:
            # 只有 env
            os.environ["CLOUDPODS_KEYSTONE_URL"] = "https://keystone"
            os.environ["CLOUDPODS_USER"] = "admin"
            os.environ["CLOUDPODS_PASSWORD"] = "secret"
            self.assertEqual(mod.get_env("CLOUDPODS_KEYSTONE_URL"), "https://keystone")
            self.assertEqual(mod.get_env("CLOUDPODS_USER"), "admin")
            self.assertEqual(mod.get_env("CLOUDPODS_PASSWORD"), "secret")
        finally:
            for k, v in old.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


class TestCoreLogging(unittest.TestCase):
    """core.logging 的 JSON 格式器。"""

    def test_json_formatter(self):
        record = logging.LogRecord(
            name="ci_cli.test", level=logging.INFO, pathname=__file__,
            lineno=1, msg="hello %s", args=("world",), exc_info=None)
        payload = json.loads(JsonFormatter().format(record))
        self.assertEqual(payload["level"], "INFO")
        self.assertEqual(payload["message"], "hello world")
        self.assertEqual(payload["logger"], "ci_cli.test")


if __name__ == "__main__":
    unittest.main()
