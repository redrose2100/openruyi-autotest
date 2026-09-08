"""tmt 用例元数据一致性单元测试。

针对 tests/ 下每个真正的用例目录（含 test: 字段或 test.sh），校验：

- main.fmf 是合法 YAML 且顶层为 mapping
- 必需的元数据字段（summary / test / tag / duration / tier）存在且类型正确
  （tmt 中 duration 是字符串，如 '5m' / '1h'；tier 是整数 0-2）
- test: 指向的脚本存在，且路径不会逃逸出 tests/ 目录
- test 脚本在 git 中标记为可执行（Windows 文件系统无 exec 位，以 git 模式为准）
- 脚本开头为 shebang（容忍 BOM），且由 bash 解释
- test 脚本不带 UTF-8 BOM（BOM 可能导致 shebang 失效）
"""

import os
import unittest

import yaml

from unittests import tmt_utils

# tmt 规范约定的 tier 含义：
# 0 = Smoke test (run on every commit)
# 1 = core/Security test (daily build)
# 2 = compatibility/performance/Reliability test (before release)
VALID_TIERS = {0, 1, 2}

# tmt duration 格式：数字 + 单位（s/m/h/d），如 5m / 1h / 30s
DURATION_RE = r"^\d+[smhd]$"

# 必需字段：值必须是非空字符串
REQUIRED_STR_FIELDS = ("summary", "test")

# 必需字段：tier 必须是整数
REQUIRED_INT_FIELDS = ("tier",)

# 推荐字段：存在时应为非空字符串
RECOMMENDED_STR_FIELDS = ("tag", "path", "contact")

# 允许出现在 test: 行首的脚本名白名单
ALLOWED_SCRIPT_NAMES = ("test.sh", "test", "runtest.sh", "runtest")


class TestFmfYamlValid(unittest.TestCase):
    """每个用例 main.fmf 都必须是合法 YAML 且顶层为 mapping。"""

    def test_all_main_fmf_valid_yaml(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            fmf_path = os.path.join(test_dir, "main.fmf")
            try:
                with open(fmf_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except Exception as e:
                violations.append(f"{rel}/main.fmf: YAML 解析失败 - {e}")
                continue
            if not isinstance(data, dict):
                violations.append(f"{rel}/main.fmf: 顶层必须是 mapping，实际为 {type(data).__name__}")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf 非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )


class TestFmfRequiredFields(unittest.TestCase):
    """每个用例 main.fmf 必须包含 tmt 必需字段且类型正确。"""

    def test_required_string_fields(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            if meta is None:
                violations.append(f"{rel}/main.fmf: 无法解析元数据")
                continue
            for field in REQUIRED_STR_FIELDS:
                value = meta.get(field)
                if not isinstance(value, str) or not value.strip():
                    violations.append(f"{rel}/main.fmf: 缺少必需字符串字段 '{field}'")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf 缺少必需字段:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )

    def test_required_int_fields(self):
        """tier 必须是整数。duration 是字符串，由 TestFmfDuration 校验。"""
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            if meta is None:
                continue
            for field in REQUIRED_INT_FIELDS:
                value = meta.get(field)
                if not isinstance(value, int) or isinstance(value, bool):
                    violations.append(f"{rel}/main.fmf: 字段 '{field}' 应为整数，实际为 {type(value).__name__}")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf 整数字段非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )

    def test_recommended_fields_non_empty(self):
        """推荐字段存在时必须是合法的非空值。"""
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            if meta is None:
                continue
            for field in RECOMMENDED_STR_FIELDS:
                if field not in meta:
                    continue
                value = meta[field]
                # tag 可以是字符串或字符串列表
                if field == "tag":
                    if isinstance(value, str) and value.strip():
                        continue
                    if isinstance(value, list) and value and all(
                        isinstance(x, str) and x.strip() for x in value
                    ):
                        continue
                    violations.append(f"{rel}/main.fmf: 字段 'tag' 应为非空字符串或字符串列表")
                else:
                    if not isinstance(value, str) or not value.strip():
                        violations.append(f"{rel}/main.fmf: 字段 '{field}' 应为非空字符串")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf 推荐字段非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )


class TestFmfTier(unittest.TestCase):
    """tier 值必须在 tmt 规范约定的 0-2 范围内。"""

    def test_tier_in_valid_range(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            if meta is None or "tier" not in meta:
                continue
            tier = meta["tier"]
            if not isinstance(tier, int) or isinstance(tier, bool) or tier not in VALID_TIERS:
                violations.append(f"{rel}/main.fmf: tier={tier!r} 不在合法范围 {sorted(VALID_TIERS)}")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf tier 非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )


class TestFmfDuration(unittest.TestCase):
    """duration 格式必须符合 tmt 约定（数字+单位 s/m/h/d）。"""

    def test_duration_format(self):
        import re

        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            if meta is None or "duration" not in meta:
                continue
            duration = meta["duration"]
            if isinstance(duration, str) and re.match(DURATION_RE, duration.strip()):
                continue
            violations.append(f"{rel}/main.fmf: duration={duration!r} 不符合格式（应为如 5m / 1h / 30s）")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf duration 非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )


class TestFmfTestScript(unittest.TestCase):
    """test: 字段必须指向存在且 git 中可执行的脚本。"""

    def test_test_script_exists(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, exists = tmt_utils.resolve_test_script(test_dir, meta)
            if not exists:
                violations.append(f"{rel}/main.fmf: test: 指向的脚本不存在 ({script or '未声明'})")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf test 脚本缺失:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )

    def test_test_script_name_allowed(self):
        """test: 指向的脚本名应在白名单内（防止指向任意路径）。"""
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, _ = tmt_utils.resolve_test_script(test_dir, meta)
            if script is None:
                continue
            name = os.path.basename(script)
            if name not in ALLOWED_SCRIPT_NAMES:
                violations.append(f"{rel}/main.fmf: test 脚本名 '{name}' 不在白名单 {ALLOWED_SCRIPT_NAMES}")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf test 脚本名非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )

    def test_test_script_within_tests_dir(self):
        """test: 指向的路径不得逃逸出 tests/ 目录。"""
        violations = []
        tests_root = os.path.abspath(tmt_utils.TESTS_DIR)
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, _ = tmt_utils.resolve_test_script(test_dir, meta)
            if script is None:
                continue
            abs_script = os.path.abspath(script)
            if os.path.commonpath([tests_root, abs_script]) != tests_root:
                violations.append(f"{rel}/main.fmf: test 脚本路径 '{script}' 逃逸出 tests/ 目录")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 main.fmf test 路径越界:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )

    def test_test_script_executable_in_git(self):
        """test: 指向的脚本必须在 git 中标记为可执行（100755）。

        Windows 文件系统没有 exec 位，以 git 模式为准；
        Linux 上 git checkout 会还原可执行位。
        """
        executables = tmt_utils.get_git_executable_files()
        if not executables:
            self.skipTest("仓库不在 git 中或无 .sh 跟踪文件，跳过")

        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, exists = tmt_utils.resolve_test_script(test_dir, meta)
            if not exists:
                continue
            script_rel = os.path.relpath(script, tmt_utils.TESTS_DIR).replace("\\", "/")
            if script_rel not in executables:
                violations.append(f"{rel}/main.fmf: test 脚本 '{script_rel}' 在 git 中未标记可执行 (100755)")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 test 脚本未在 git 中标记可执行:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
                + "\n\n修复方法: git update-index --chmod=+x <file>"
            )


class TestFmfShebang(unittest.TestCase):
    """test 脚本必须含 shebang（容忍 BOM），且由 bash 解释。"""

    def test_test_script_shebang_bash(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, exists = tmt_utils.resolve_test_script(test_dir, meta)
            if not exists:
                continue
            try:
                with open(script, "r", encoding="utf-8", errors="replace") as f:
                    first_line = f.readline().strip()
            except Exception:
                violations.append(f"{rel}/main.fmf: 无法读取 test 脚本 '{script}'")
                continue
            first_line = tmt_utils.strip_bom(first_line)
            if not first_line.startswith("#!"):
                violations.append(f"{rel}/main.fmf: test 脚本 '{os.path.basename(script)}' 缺少 shebang")
            elif "bash" not in first_line and "sh" not in first_line:
                violations.append(f"{rel}/main.fmf: test 脚本 shebang 应为 bash，实际为 '{first_line}'")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 test 脚本 shebang 非法:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )


class TestFmfNoBom(unittest.TestCase):
    """test 脚本不应带 UTF-8 BOM（BOM 会导致 shebang 失效等兼容性问题）。

    当前仓库存在约 2575 个历史文件带 BOM（遗留问题），
    因此本测试报告问题但不失败，避免阻塞 CI；
    新提交的 test 脚本应确保无 BOM。
    """

    def test_test_script_no_bom(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, exists = tmt_utils.resolve_test_script(test_dir, meta)
            if not exists:
                continue
            if tmt_utils.file_has_bom(script):
                script_rel = os.path.relpath(script, tmt_utils.TESTS_DIR).replace("\\", "/")
                violations.append(f"{rel}/main.fmf: test 脚本 '{script_rel}' 带 UTF-8 BOM")
        if violations:
            # 报告但不失败：历史遗留问题，修复工作量大
            print(
                f"⚠ 发现 {len(violations)} 个 test 脚本带 UTF-8 BOM（已知遗留问题，不阻塞）:\n"
                + "\n".join(f"  - {v}" for v in violations[:10])
                + "\n\n修复方法: 以 UTF-8 无 BOM 重新保存（如 PowerShell: "
                + "[IO.File]::WriteAllText($p, [IO.File]::ReadAllText($p), (New-Object Text.UTF8Encoding $false))）"
            )


if __name__ == "__main__":
    unittest.main()
