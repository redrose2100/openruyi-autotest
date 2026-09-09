# unittests - 测试框架质量单元测试

本目录包含针对测试框架本身的单元测试，确保后续对测试用例的修改符合规范。

测试以 pytest 为统一入口，覆盖四个层面：

1. **fmf 元数据校验**（`test_fmf_metadata.py`）：对 `tests/` 下所有真用例目录
   （含 `test:` 字段或 `test.sh`）检查 `main.fmf` 的 YAML 合法性、必填字段、
   `tier` 取值范围、`duration` 格式、test 脚本存在性/可执行性、shebang 等。
2. **shell 脚本语法与结构**（`test_sh_syntax.py`）：所有 `.sh` 文件通过
   `bash -n` 语法检查；用例引用的共享库（`lib.sh` 等）路径真实存在；
   git 跟踪的用例其 test 脚本在文件系统成对存在。
3. **共享库逻辑打桩测试**（`test_lib_logic.py`）：在 bash 子进程中以
   打桩（stub）方式加载真实的 `lib.sh` / `hw_check.sh`，验证 flag-file +
   引用计数算法与纯函数行为。
4. **静态质量检查**（`test_tests_quality.py`）：中文字符、乱码、tmt 规范、可执行位。

> 说明：分组目录（如 `smoke/`、`compatibility/ltp_posix/aio/`）的 `main.fmf`
> 只提供 tmt 继承配置、没有 `test:` 字段，是合法结构，**不视为用例目录**，
> 相关检查会自动跳过它们。

## 运行方式

```bash
# 运行所有单元测试（推荐，pytest 统一入口）
python -m pytest unittests -v

# 运行单个测试文件
python -m pytest unittests/test_fmf_metadata.py -v
python -m pytest unittests/test_sh_syntax.py -v
python -m pytest unittests/test_tests_quality.py -v

# 用 unittest 发现模式运行
python -m unittest discover -s unittests -p "test_*.py" -v
```

## 依赖

- pytest（建议 7+）
- PyYAML（解析 `main.fmf`）
- bash（`bash -n` 语法检查；Windows 下自动探测 Git 安装目录，
  找不到时相关用例会 skip 而不是失败）

## 测试用例说明

### test_fmf_metadata.py（fmf 元数据）

| 用例 | 描述 |
|------|------|
| `TestFmfYamlValid` | 所有 `main.fmf` 必须是合法 YAML 且为映射 |
| `TestFmfRequiredFields` | 真用例目录的 `summary`/`test` 非空，`tier` 为整数 |
| `TestFmfTier` | `tier` 取值 ∈ {0, 1, 2} |
| `TestFmfDuration` | `duration` 格式为 `^\d+[smhd]$`（如 `5m`、`1h`） |
| `TestFmfTestScript` | `test:` 脚本存在、git 中可执行（100755）、名字合法、在 `tests/` 内 |
| `TestFmfShebang` | test 脚本以 `#!/bin/bash` 开头（容忍 BOM） |
| `TestFmfNoBom` | test 脚本不应带 UTF-8 BOM。**报告但不失败**：仓库现存约 2575 个历史文件带 BOM，属已知遗留问题，修复量大，先以统计输出方式暴露，避免阻塞 CI |

### test_sh_syntax.py（shell 语法与结构）

| 用例 | 描述 |
|------|------|
| `TestShSyntax::test_all_sh_syntax_valid` | 所有 `.sh` 通过 `bash -n`（约 4300+ 文件，运行约 5-6 分钟） |
| `TestLibReferenceConsistency` | 用例脚本中 `. "$(dirname "$0")/xxx/lib.sh"` 形式的引用目标真实存在 |
| `TestGitTrackedConsistency` | git 跟踪的真用例目录其 `test:` 脚本在文件系统存在 |

### test_lib_logic.py（共享库逻辑打桩）

| 用例 | 描述 |
|------|------|
| `TestLibFlagRefLogic::test_all_libs_have_flag_ref_pattern` | 所有 `lib.sh` 都具备 FLAG 变量 + Setup/Cleanup 函数 |
| `TestLibFlagRefLogic::test_first_setup_creates_flag_ref1` | 首次 Setup 创建 flag 文件且 `ref=1` |
| `TestLibFlagRefLogic::test_second_setup_increments_ref` | 再次 Setup 递增 `ref`（1→2） |
| `TestLibFlagRefLogic::test_cleanup_decrements_ref` | Cleanup 递减 `ref`（2→1） |
| `TestLibFlagRefLogic::test_cleanup_last_removes_flag` | 最后一次 Cleanup 删除 flag 文件 |
| `TestLibFlagRefLogic::test_cleanup_without_setup_noop` | 未 Setup 直接 Cleanup 为 no-op |
| `TestHwCheckFunctions` | `hw_check.sh` 的 `_hwParseOp`（操作符解析）与 `_hwCompare`（数值/字符串比较）纯函数 |

> 实现要点：测试不修改任何生产 `lib.sh`，而是在 bash 子进程中先注入 Beakerlib
> 与系统命令的 stub（`rlLogInfo`/`rlCleanupAppend`/`rpm`/`dnf`/`curl` 等），
> 再 source 真实库文件，最后把 FLAG 变量覆盖到临时目录，从而验证真实的
> 引用计数算法。该文件约 9 分钟（241 个 lib.sh × 6 种场景 × bash 子进程开销）。

### test_tests_quality.py（静态质量）

| 用例 | 描述 |
|------|------|
| `test_no_chinese` | `tests/` 下所有文件不含中文字符 |
| `test_no_mojibake` | `tests/` 下所有文件无乱码 |
| `test_sh_tmt_compliance` | 所有 `.sh` 符合 tmt 测试框架规范 |
| `test_sh_executable` | 所有 `.sh` 具有可执行权限（Windows 上按 git 模式位 100755 判定） |

## 公共工具（tmt_utils.py）

`unittests/tmt_utils.py` 提供共享工具：用例目录收集（`collect_real_test_dirs` 自动
排除分组目录）、`main.fmf` 解析、test 脚本解析、git 可执行位查询（`get_git_executable_files`）、
bash 探测与 `bash -n` 执行等。新测试请优先复用。

## 已知遗留问题

- **2575 个 test 脚本带 UTF-8 BOM**（约 63%）：BOM 可能导致 shebang 失效。
  `TestFmfNoBom` 仅报告不失败。修复方式：以 UTF-8 无 BOM 重新保存全部受影响文件
  （如 PowerShell: `[IO.File]::WriteAllText($p, [IO.File]::ReadAllText($p), (New-Object Text.UTF8Encoding $false))`），
  修复后可将该用例恢复为硬失败。

## CI 集成

GitHub Actions 工作流 `.github/workflows/unit-tests.yml` 在每次 push/PR 时运行：

| Job | 内容 | 预计耗时 |
|-----|------|----------|
| `quick` | `test_fmf_metadata.py`（fmf 元数据） | ~1 分钟 |
| `full` | `test_lib_logic.py` + `test_sh_syntax.py` + `test_tests_quality.py` | ~25 分钟 |

两个 job 并行执行，任一失败即阻断合并。本地可分别用
`python -m pytest unittests/test_fmf_metadata.py -q` 与
`python -m pytest unittests/ -q` 复现。
