"""共享库（lib.sh / hw_check.sh）逻辑打桩单元测试。

策略说明
--------
这些库设计为在 tmt/Beakerlib 环境中运行，直接执行会触发系统命令
（rpm/dnf/sudo/sshpass 等），无法在单元测试环境真实执行。

因此本测试采用「打桩 + 真实逻辑」方式：

- 在 bash 子进程中 source 真实的 lib.sh（保证测的是仓库真实逻辑）
- 但先注入 stub：rlLogInfo/rlCleanupAppend 为 no-op，
  rpm 返回"已安装"（避免触发安装），dnf/sudo 为 no-op
- source 之后把 FLAG 变量覆盖为临时目录路径（不碰 /tmp 真实 flag）
- 然后调用真实函数，验证引用计数算法行为

覆盖：
1. flag-file + 引用计数模式（241 个 lib.sh 的统一模式）：
   - 首次 Setup 创建 flag（ref=1）
   - 再次 Setup 递增 ref
   - Cleanup 递减 ref
   - ref 归零删除 flag
   - 未 Setup 直接 Cleanup 为 no-op
2. hw_check.sh 纯函数：
   - _hwParseOp（操作符解析）
   - _hwCompare（数值/字符串比较）
"""

import os
import re
import subprocess
import tempfile
import unittest

from unittests import tmt_utils

BASH = tmt_utils.find_bash()


def _find_all_lib_files():
    """收集 tests/ 下所有 lib.sh 绝对路径。"""
    libs = []
    for dirpath, dirnames, filenames in os.walk(tmt_utils.TESTS_DIR):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn == "lib.sh":
                libs.append(os.path.join(dirpath, fn))
    return sorted(libs)


def _extract_flag_var(lib_path):
    """从 lib.sh 提取 FLAG 变量名和 Setup 函数名前缀。

    例：LTP_FLAG + ltpPosixSetup -> (LTP_FLAG, ltpPosix)
    返回 (var, func_prefix) 或 None。
    """
    with open(lib_path, encoding="utf-8", errors="replace") as f:
        content = f.read()
    m = re.search(r"^([A-Za-z_][A-Za-z0-9_]*FLAG)=\"", content, re.MULTILINE)
    if not m:
        return None
    var = m.group(1)
    # 直接提取实际的 Setup 函数名（正则已把 Setup 排除在捕获组外，
    # 因此 group(1) 即前缀，如 ltpPosixSetup -> ltpPosix）
    sm = re.search(r"\b([A-Za-z_][A-Za-z0-9_]*)Setup\(\)", content)
    if not sm:
        return None
    func_prefix = sm.group(1)
    return var, func_prefix


def run_lib_scenario(lib_path, scenario_body, timeout=60):
    """在打桩环境中运行 lib.sh 逻辑。

    场景脚本（scenario_body）中可用 {FLAG} 占位符引用 FLAG 变量名。
    返回 dict(returncode, stdout, stderr)。
    """
    if BASH is None:
        return None

    tmpdir = tempfile.mkdtemp(prefix="libtest_")
    var, _prefix = _extract_flag_var(lib_path) or ("FLAG", "lib")
    flag_path = os.path.join(tmpdir, "flag").replace("\\", "/")
    scenario = scenario_body.replace("{FLAG}", f"${{{var}}}")

    script = f"""
# ---- stubs: Beakerlib & 系统命令 ----
rlLogInfo() {{ :; }}
rlLogWarning() {{ :; }}
rlLogError() {{ :; }}
rlCleanupAppend() {{ :; }}
rlPass() {{ :; }}
rlFail() {{ return 1; }}
rlRun() {{ eval "$1"; return 0; }}
rlTestSkip() {{ return 0; }}
rlPhaseStartSetup() {{ :; }}
rlJournalEnd() {{ :; }}
rpm() {{ return 0; }}
sudo() {{ :; }}
dnf() {{ return 1; }}
yum() {{ return 1; }}
apt-get() {{ return 1; }}
hostname() {{ echo testhost; }}
nproc() {{ echo 8; }}
free() {{ echo "Mem: 1 2 3 4 5 6 7"; }}
lsblk() {{ echo sda; }}
ip() {{ echo "2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> state UP"; }}
curl() {{
    # 解析 -o <path> 并真实创建文件，模拟真实下载
    local out=""
    while [ "$#" -gt 0 ]; do
        if [ "$1" = "-o" ] && [ "$#" -gt 1 ]; then
            out="$2"; shift 2
        else
            shift
        fi
    done
    if [ -n "$out" ]; then echo "stub-download-content" > "$out"; fi
    return 0
}}
sha256sum() {{ echo "0f5642a5ecbecc79e79aa3a1ab015c2e77d0027c51938fee7d5ac9d8dfd166be  /tmp/sonobuoy"; }}
install() {{ :; }}
sonobuoy() {{ echo "sonobuoy v0.57.3"; }}

# ---- source 真实库 ----
source "{lib_path}"

# ---- 覆盖 FLAG 到临时目录（不碰 /tmp） ----
{var}="{flag_path}"

# ---- 场景 ----
set -u
{scenario}
"""
    try:
        result = subprocess.run(
            [BASH, "-c", script],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "timeout"}
    except Exception as e:  # pragma: no cover
        return {"returncode": -2, "stdout": "", "stderr": str(e)}


@unittest.skipIf(BASH is None, "未找到 bash 解释器")
class TestLibFlagRefLogic(unittest.TestCase):
    """flag-file + 引用计数模式的核心算法验证。"""

    @classmethod
    def setUpClass(cls):
        cls.libs = _find_all_lib_files()
        cls.flag_vars = {}
        for lib in cls.libs:
            info = _extract_flag_var(lib)
            if info:
                cls.flag_vars[lib] = info

    def test_all_libs_have_flag_ref_pattern(self):
        """所有 lib.sh 都应具备 FLAG + Setup + Cleanup 模式。"""
        missing = []
        for lib in self.libs:
            with open(lib, encoding="utf-8", errors="replace") as f:
                content = f.read()
            has_setup = re.search(r"\b\w+Setup\(\)", content) is not None
            has_cleanup = re.search(r"\b\w+Cleanup\(\)", content) is not None
            if not has_setup or not has_cleanup:
                missing.append(os.path.relpath(lib, tmt_utils.TESTS_DIR))
        for lib in self.libs:
            if lib not in self.flag_vars:
                missing.append(os.path.relpath(lib, tmt_utils.TESTS_DIR))
        if missing:
            self.fail(
                f"{len(missing)} 个 lib.sh 缺少 FLAG/Setup/Cleanup 模式:\n"
                + "\n".join(f"  - {v}" for v in missing[:20])
            )

    # ---- 用每个 lib.sh 验证引用计数算法 ----

    def test_first_setup_creates_flag_ref1(self):
        """首次 Setup 应创建 flag 文件且 ref=1（对所有 lib.sh）。"""
        for lib, (var, prefix) in self.flag_vars.items():
            rel = os.path.relpath(lib, tmt_utils.TESTS_DIR)
            scenario = f"""
{prefix}Setup
if [ ! -f {{FLAG}} ]; then echo "NO_FLAG"; exit 1; fi
grep -q "^ref=1$" {{FLAG}} && echo "REF1_OK"
"""
            res = run_lib_scenario(lib, scenario)
            if res is None:
                self.skipTest("bash 不可用")
            self.assertEqual(
                res["returncode"], 0, f"[{rel}] {res['stdout']} {res['stderr']}"
            )
            self.assertIn("REF1_OK", res["stdout"], f"[{rel}] ref 应为 1")

    def test_second_setup_increments_ref(self):
        """再次 Setup 应递增 ref（对所有 lib.sh）。"""
        for lib, (var, prefix) in self.flag_vars.items():
            rel = os.path.relpath(lib, tmt_utils.TESTS_DIR)
            scenario = f"""
{prefix}Setup
{prefix}Setup
ref=$(grep "^ref=" {{FLAG}} | cut -d= -f2)
[ "$ref" = "2" ] && echo "REF2_OK" || echo "REF=$ref"
"""
            res = run_lib_scenario(lib, scenario)
            self.assertEqual(
                res["returncode"], 0, f"[{rel}] {res['stdout']} {res['stderr']}"
            )
            self.assertIn("REF2_OK", res["stdout"], f"[{rel}] ref 应为 2")

    def test_cleanup_decrements_ref(self):
        """Cleanup 应递减 ref（对所有 lib.sh）。"""
        for lib, (var, prefix) in self.flag_vars.items():
            rel = os.path.relpath(lib, tmt_utils.TESTS_DIR)
            scenario = f"""
{prefix}Setup
{prefix}Setup
{prefix}Cleanup
ref=$(grep "^ref=" {{FLAG}} | cut -d= -f2)
[ "$ref" = "1" ] && echo "REF1_OK" || echo "REF=$ref"
"""
            res = run_lib_scenario(lib, scenario)
            self.assertEqual(
                res["returncode"], 0, f"[{rel}] {res['stdout']} {res['stderr']}"
            )
            self.assertIn("REF1_OK", res["stdout"], f"[{rel}] Cleanup 后 ref 应为 1")

    def test_cleanup_last_removes_flag(self):
        """最后一次 Cleanup 应删除 flag 文件（对所有 lib.sh）。"""
        for lib, (var, prefix) in self.flag_vars.items():
            rel = os.path.relpath(lib, tmt_utils.TESTS_DIR)
            scenario = f"""
{prefix}Setup
{prefix}Cleanup
if [ -f {{FLAG}} ]; then echo "STILL_EXISTS"; else echo "REMOVED"; fi
"""
            res = run_lib_scenario(lib, scenario)
            self.assertEqual(
                res["returncode"], 0, f"[{rel}] {res['stdout']} {res['stderr']}"
            )
            self.assertIn("REMOVED", res["stdout"], f"[{rel}] Cleanup 后 flag 应被删除")

    def test_cleanup_without_setup_noop(self):
        """未 Setup 直接 Cleanup 应为 no-op（对所有 lib.sh）。"""
        for lib, (var, prefix) in self.flag_vars.items():
            rel = os.path.relpath(lib, tmt_utils.TESTS_DIR)
            scenario = f"""
{prefix}Cleanup
echo "NOOP_OK"
"""
            res = run_lib_scenario(lib, scenario)
            self.assertEqual(
                res["returncode"], 0, f"[{rel}] {res['stdout']} {res['stderr']}"
            )
            self.assertIn("NOOP_OK", res["stdout"], f"[{rel}] 未 Setup 的 Cleanup 应 no-op")


@unittest.skipIf(BASH is None, "未找到 bash 解释器")
class TestHwCheckFunctions(unittest.TestCase):
    """hw_check.sh 纯函数打桩测试。"""

    HW_CHECK = os.path.join(tmt_utils.TESTS_DIR, "lib", "hw_check.sh")

    def run_hw(self, bash_code):
        """在打桩环境中加载 hw_check.sh 并执行 bash_code，返回 stdout。"""
        stub = "rlLogInfo() { :; }\nrlLogWarning() { :; }\n"
        full = stub + f'source "{self.HW_CHECK}"\n' + bash_code
        result = subprocess.run(
            [BASH, "-c", full],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_parse_op_ge(self):
        self.assertIn(">=|4", self.run_hw("_hwParseOp '>= 4'"))

    def test_parse_op_le(self):
        self.assertIn("<=|2", self.run_hw("_hwParseOp '<= 2'"))

    def test_parse_op_eq(self):
        self.assertIn("=|8", self.run_hw("_hwParseOp '= 8'"))

    def test_parse_op_gt(self):
        self.assertIn(">|1", self.run_hw("_hwParseOp '> 1'"))

    def test_parse_op_lt(self):
        self.assertIn("<|3", self.run_hw("_hwParseOp '< 3'"))

    def test_parse_op_ne(self):
        self.assertIn("!=|2", self.run_hw("_hwParseOp '!= 2'"))

    def test_parse_op_default_eq(self):
        """无操作符时默认 '='。"""
        self.assertIn("=|4", self.run_hw("_hwParseOp '4'"))

    def test_parse_op_strip_quotes(self):
        """值中的引号应被剥离。"""
        self.assertIn(">=|4", self.run_hw("_hwParseOp '>= \"4\"'"))

    def test_compare_int_ge_true(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 5 '>= 4' int && echo TRUE || echo FALSE"))

    def test_compare_int_ge_false(self):
        self.assertIn("FALSE", self.run_hw("_hwCompare 3 '>= 4' int && echo TRUE || echo FALSE"))

    def test_compare_int_lt(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 2 '< 4' int && echo TRUE || echo FALSE"))

    def test_compare_int_eq(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 4 '= 4' int && echo TRUE || echo FALSE"))

    def test_compare_int_ne(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 4 '!= 5' int && echo TRUE || echo FALSE"))

    def test_compare_int_le(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 4 '<= 4' int && echo TRUE || echo FALSE"))

    def test_compare_str_eq(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 'foo' '= foo' str && echo TRUE || echo FALSE"))

    def test_compare_str_ne(self):
        self.assertIn("TRUE", self.run_hw("_hwCompare 'foo' '!= bar' str && echo TRUE || echo FALSE"))

    def test_compare_str_unsupported_op(self):
        """字符串比较不支持 > <，应返回失败。"""
        self.assertIn("FALSE", self.run_hw("_hwCompare 'foo' '> a' str && echo TRUE || echo FALSE"))

    def test_compare_int_unsupported_op(self):
        self.assertIn("FALSE", self.run_hw("_hwCompare 5 '~ 4' int && echo TRUE || echo FALSE"))


if __name__ == "__main__":
    unittest.main()
