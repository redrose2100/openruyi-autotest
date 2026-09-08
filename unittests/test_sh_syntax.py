"""tmt 用例 shell 脚本语法与结构单元测试。

针对 tests/ 下所有 .sh 文件：

- bash -n 语法检查通过（这是性价比最高的一层，能抓 90% 的提交错误）
- 被用例引用的共享库 lib.sh 路径正确（相对于用例目录解析）
- git 跟踪的用例目录（含 test: 字段）其脚本在文件系统存在

说明：分组目录（如 smoke/、compatibility/ltp_posix/aio/）的 main.fmf
只提供继承配置，没有 test: 字段，是 tmt 合法结构，不视为用例。
"""

import os
import re
import unittest

from unittests import tmt_utils


class TestShSyntax(unittest.TestCase):
    """tests/ 下所有 .sh 文件必须通过 bash -n 语法检查。"""

    def test_all_sh_syntax_valid(self):
        bash = tmt_utils.find_bash()
        if bash is None:
            self.skipTest("未找到 bash 解释器，跳过语法检查")

        all_sh = []
        for dirpath, dirnames, filenames in os.walk(tmt_utils.TESTS_DIR):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for fn in filenames:
                if fn.endswith(".sh"):
                    all_sh.append(os.path.join(dirpath, fn))

        failures = []
        for script in sorted(all_sh):
            rel = os.path.relpath(script, tmt_utils.TESTS_DIR).replace("\\", "/")
            ok, msg = tmt_utils.run_bash_syntax_check(script, bash=bash)
            if not ok:
                failures.append(f"{rel}: {msg}")

        if failures:
            self.fail(
                f"发现 {len(failures)} 个 .sh 文件语法错误:\n"
                + "\n".join(f"  - {v}" for v in failures[:30])
            )


class TestLibReferenceConsistency(unittest.TestCase):
    """被用例引用的共享库 lib.sh 必须真实存在于预期位置。"""

    def test_referenced_libs_exist(self):
        """扫描每个用例目录内 .sh 中的相对 source/'.' 引用，验证目标存在。"""
        missing = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            test_script = os.path.join(test_dir, "test.sh")
            if not os.path.isfile(test_script):
                continue
            try:
                with open(test_script, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception:
                continue
            # 匹配 . "$(dirname "$0")/xxx/lib.sh" 或 . ./xxx/lib.sh 形式的引用
            for match in _find_dot_sources(content):
                # 引用形如 ../lib.sh 或 ../../lib/hw_check.sh，相对于用例目录解析
                target = os.path.normpath(os.path.join(test_dir, match))
                if not os.path.isfile(target):
                    missing.append(f"{rel}/test.sh 引用 {match} 不存在 ({target})")
        if missing:
            self.fail(
                f"发现 {len(missing)} 个共享库引用缺失:\n"
                + "\n".join(f"  - {v}" for v in missing[:30])
            )


def _find_dot_sources(content):
    """从脚本内容中提取相对 source/'.' 引用的相对路径。

    支持的形态：
      . "$(dirname "$0")/../lib.sh"
      . ./lib.sh
      source ../lib.sh
    返回去引号后的相对路径列表。
    """
    results = []
    # 形态 1: . "$(dirname "$0")/<rel>" 或 source "$(dirname "$0")/<rel>"
    pattern1 = re.compile(
        r'^(?:\s*\.|\s*source)\s+"\$\(dirname\s+"?\$0"?\)/([^"]+)"',
        re.MULTILINE,
    )
    for m in pattern1.finditer(content):
        rel = m.group(1)
        # 去掉可能的尾部引号/空格
        rel = rel.strip().strip('"')
        results.append(rel)
    # 形态 2: . ./rel 或 source ./rel（不带 $(dirname)）
    pattern2 = re.compile(r'^(?:\s*\.|\s*source)\s+(\./[^\s"\';#]+)', re.MULTILINE)
    for m in pattern2.finditer(content):
        results.append(m.group(1).strip())
    return results


class TestGitTrackedConsistency(unittest.TestCase):
    """git 跟踪的用例（含 test: 字段）其脚本应成对存在。"""

    def test_tracked_test_scripts_present(self):
        """git 中跟踪的每个真用例目录，其 test: 脚本必须在文件系统存在。"""
        tracked = tmt_utils.get_git_ls_files()
        if not tracked:
            self.skipTest("仓库不在 git 中或无跟踪文件，跳过")

        # 找出 git 跟踪的、真正的用例目录（含 test: 字段或 test.sh）
        tracked_dirs = set()
        for rel in tracked:
            if rel.endswith("main.fmf"):
                d = os.path.normpath(os.path.join(tmt_utils.TESTS_DIR, os.path.dirname(rel)))
                if d != tmt_utils.TESTS_DIR and tmt_utils.is_test_dir(d):
                    tracked_dirs.add(d)

        violations = []
        for test_dir in sorted(tracked_dirs):
            rel = os.path.relpath(test_dir, tmt_utils.TESTS_DIR).replace("\\", "/")
            _, meta = tmt_utils.get_test_metadata(test_dir)
            script, exists = tmt_utils.resolve_test_script(test_dir, meta)
            if not exists:
                violations.append(f"{rel}/main.fmf: test 脚本缺失（git 中已跟踪该用例）")
        if violations:
            self.fail(
                f"发现 {len(violations)} 个 git 跟踪用例缺少 test 脚本:\n"
                + "\n".join(f"  - {v}" for v in violations[:30])
            )


if __name__ == "__main__":
    unittest.main()
