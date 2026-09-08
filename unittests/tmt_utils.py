"""tmt 测试用例目录的公共工具函数。

供 unittests/ 下的测试文件复用：

- 递归收集 tests/ 下所有含 main.fmf 的用例目录
- 解析 main.fmf（YAML）元数据
- 定位用例的 test 脚本 / 共享库
- 探测系统可用的 bash 解释器
"""

import os
import shutil
import subprocess

# 项目根目录（本文件位于 unittests/ 下）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")


def collect_test_dirs(root_dir=None):
    """递归收集 root_dir 下所有包含 main.fmf 的目录，返回绝对路径列表。

    顶层 tests/main.fmf 是全局共享配置，本身不构成用例目录，
    因此要求目录内除 main.fmf 外还有实际内容，且跳过 TESTS_DIR 本身。
    """
    root_dir = root_dir or TESTS_DIR
    result = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过隐藏目录
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if "main.fmf" in filenames and dirpath != root_dir:
            result.append(dirpath)
    return sorted(result)


def is_test_dir(test_dir):
    """判断目录是否为真正的用例目录（而非仅含继承配置的分组目录）。

    分组目录（如 smoke/、compatibility/ltp_posix/aio/）只有 main.fmf 提供
    继承配置，没有 test 脚本；用例目录必须有 test: 字段或 test.sh。
    """
    if os.path.isfile(os.path.join(test_dir, "test.sh")):
        return True
    _, meta = get_test_metadata(test_dir)
    return bool(meta and isinstance(meta.get("test"), str) and meta.get("test").strip())


def collect_real_test_dirs(root_dir=None):
    """收集真正的用例目录（排除分组/继承配置目录）。"""
    return [d for d in collect_test_dirs(root_dir) if is_test_dir(d)]



def _parse_fmf(filepath):
    """解析单个 main.fmf 文件，返回 dict。

    解析失败返回 None（由调用方决定如何报告）。
    """
    try:
        import yaml
    except ImportError:
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def get_test_metadata(test_dir):
    """返回 (test_dir, metadata_dict) 或 (test_dir, None)。"""
    fmf_path = os.path.join(test_dir, "main.fmf")
    return test_dir, _parse_fmf(fmf_path)


def resolve_test_script(test_dir, metadata):
    """解析 main.fmf 中 test: 字段指向的脚本路径。

    返回 (绝对路径, 是否存在)。test: 字段可含参数（如 './test.sh arg'），
    仅取第一个 token。无法解析时返回 (None, False)。
    """
    if not metadata:
        return None, False
    test_value = metadata.get("test")
    if not isinstance(test_value, str) or not test_value.strip():
        return None, False
    first = test_value.strip().split()[0]
    script = os.path.normpath(os.path.join(test_dir, first))
    return script, os.path.isfile(script)


def strip_bom(text):
    """去掉字符串开头的 UTF-8 BOM（\ufeff），便于 shebang 等判断。"""
    if text.startswith("\ufeff"):
        return text[1:]
    return text


def file_has_bom(filepath):
    """检测文件是否以 UTF-8 BOM 开头。"""
    try:
        with open(filepath, "rb") as f:
            return f.read(3) == b"\xef\xbb\xbf"
    except Exception:
        return False


def get_git_executable_files(root_dir=TESTS_DIR):
    """获取 git 中标记为可执行的 .sh 文件集合（相对于 TESTS_DIR 的正斜杠路径）。

    通过 git ls-files --stage 读取模式位（100755 = 可执行）。
    仓库未初始化时返回空集。
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", "tests/*.sh", "tests/**/*.sh"],
            capture_output=True, text=True, cwd=PROJECT_ROOT, timeout=60,
        )
        if result.returncode != 0:
            return set()
        executables = set()
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            # 格式: 100755 <hash> 0\t<path>
            parts = line.split("\t")
            if len(parts) >= 2:
                mode_info = parts[0].split()
                if mode_info and mode_info[0] == "100755":
                    path = parts[1].replace("\\", "/")
                    # 转成相对于 TESTS_DIR 的路径
                    if path.startswith("tests/"):
                        path = path[len("tests/"):]
                    executables.add(path)
        return executables
    except Exception:
        return set()



def find_lib_files(test_dir):
    """向上查找用例目录树中所有 lib.sh / lib/*.sh 共享库。

    返回相对于 TESTS_DIR 的路径列表（正斜杠），用于一致性校验。
    仅收集含 main.fmf 的层级，避免误收其他目录。
    """
    libs = []
    rel = os.path.relpath(test_dir, TESTS_DIR)
    parts = rel.split(os.sep)
    for i in range(len(parts)):
        base = os.path.join(TESTS_DIR, *parts[: i + 1])
        # 只遍历到含 main.fmf 的层级的兄弟 lib.sh，不深入子目录
        for fn in sorted(os.listdir(base)):
            if fn.endswith(".sh") and os.path.isfile(os.path.join(base, fn)):
                full = os.path.join(base, fn)
                libs.append(os.path.relpath(full, TESTS_DIR).replace("\\", "/"))
    return sorted(set(libs))


def find_bash():
    """探测可用的 bash 解释器。

    优先使用 PATH 中的 bash；Windows 上常见于 Git 安装目录。
    返回可执行文件路径或 None。
    """
    found = shutil.which("bash")
    if found:
        return found
    candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
        r"C:\ProgrameFile\Git\bin\bash.exe",
        r"C:\ProgrameFile\Git\usr\bin\bash.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\bash.exe"),
        "/usr/bin/bash",
        "/bin/bash",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def run_bash_syntax_check(script_path, bash=None):
    """对脚本执行 bash -n 语法检查。

    返回 (ok, message)。
    """
    bash = bash or find_bash()
    if bash is None:
        return False, "未找到 bash 解释器"
    try:
        result = subprocess.run(
            [bash, "-n", script_path],
            capture_output=True, text=True, timeout=30,
        )
    except Exception as e:
        return False, f"执行 bash -n 失败: {e}"
    if result.returncode == 0:
        return True, ""
    return False, (result.stderr or result.stdout).strip()


def get_git_ls_files(root_dir=TESTS_DIR):
    """返回 git 跟踪的 tests/ 下文件集合（相对于 TESTS_DIR 的正斜杠路径）。

    git ls-files 输出的路径带 tests/ 前缀，这里统一剥离，
    与 get_git_executable_files() 的基线保持一致。
    仓库未初始化或不在 git 中时返回空集。
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", root_dir],
            capture_output=True, text=True, cwd=PROJECT_ROOT, timeout=60,
        )
        if result.returncode != 0:
            return set()
        paths = set()
        for f in result.stdout.splitlines():
            if not f.strip():
                continue
            path = f.replace("\\", "/")
            if path.startswith("tests/"):
                path = path[len("tests/"):]
            paths.add(path)
        return paths
    except Exception:
        return set()
