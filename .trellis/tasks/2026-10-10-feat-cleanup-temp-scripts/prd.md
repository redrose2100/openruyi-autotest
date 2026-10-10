# chore: 删除仓库根目录下的临时脚本和数据文件

## 目标

删除仓库根目录下 18 个一次性临时脚本和数据文件。这些文件创建于 Round4 CI 修复（fe102b98a）和测试拆分工作（68f97cfde）期间，均已完成其使命。生成的测试文件已落地到 `tests/functional/pkgs/` 目录，代码修复已应用。仓库中无任何其他文件引用这些文件。

## 需求

### R1：删除一次性 Python 分析/修复脚本
删除 14 个 `.py` 文件，用于一次性诊断和批量修复：
`_analyze_fails.py`、`_check_gcc.py`、`_check_tests.py`、`_fix_error_pattern.py`、`_fix_version_help.py`、`coverage_analyzer.py`、`coverage_analyzer_v2.py`、`fix_and_cleanup_coreutils.py`、`gen_curl_tests.py`、`gen_p0_tests.py`、`gen_p1_tests.py`、`gen_p3_tests.py`、`gen_p3b_tests.py`、`split_coreutils_tests.py`

### R2：删除一次性 PowerShell 分析脚本
删除 `analyze_libs.ps1` 和 `analyze_pkgs.ps1`。

### R3：删除一次性数据文件
删除 `ci_log_round4.txt` 和 `pkg_list.txt`。

### R4：确保无残留引用
验证仓库中无任何其他文件引用被删除的文件。

## 测试点

- TP1：18 个文件已从工作树中删除
- TP2：`git status` 确认 18 个删除已提交
- TP3：仓库 grep 确认 `.venv/` 之外无残留引用
- TP4：`tests/functional/pkgs/` 中的测试保持完整（生成产物不受影响）

## 验收标准

- [x] 18 个临时文件已删除
- [x] 无残留引用
- [x] 现有测试不受影响
