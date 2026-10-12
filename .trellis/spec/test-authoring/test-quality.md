# 测试质量标准

> 测试用例的完整性、正确性和可维护性标准。

---

## 功能覆盖

### 每个功能点必须覆盖

- ✅ **正向测试**（happy path）：正常输入 → 期望成功（exit 0）
- ✅ **版本/帮助测试**：`--version` 和 `--help` 能正常输出
- ✅ **基本功能测试**：核心命令的关键参数

### 推荐的补充覆盖

- 错误输入 → 期望失败（exit ≠ 0）或合理错误输出
- 边界值测试：空输入、极大值、特殊字符
- 并发/竞态场景（如果适用）

---

## 质量检查清单

`unittests/test_tests_quality.py` 自动检查以下项：

| 检查项 | 说明 |
|--------|------|
| 中文字符 | 代码中不应出现中文（注释允许，但描述应放在 rlRun 第三个参数中） |
| 乱码检测 | 禁止 GBK 乱码或非 UTF-8 内容 |
| 可执行位 | test 脚本在 git 中标记为可执行 |
| tmt 规范 | `test:` 路径不逃逸出 `tests/` 目录 |

```bash
python -m pytest unittests/test_tests_quality.py -v
```

---

## 测试原则

### "一个文件 = 一个功能点"

```
❌ 错误：一个 test.sh 测多个功能
test_coreutils_all.sh  → 同时测 cp、mv、rm、ls...

✅ 正确：拆分到独立目录
test_coreutils_cp/     → 只测 cp
test_coreutils_mv/     → 只测 mv
test_coreutils_rm/     → 只测 rm
```

**好处**：
- 单测失败直接定位到具体功能和具体命令
- CI 报告中一眼看到哪个功能出了问题
- 添加新功能只需加一个新目录，不影响已有测试

---

## 命名规范

### 目录命名

```
test_<包名>_<功能描述>
```

- 包名：小写，用下划线替代连字符（`coreutils`、`cloud-utils-growpart` → `cloud_utils_growpart`）
- 功能描述：小写，下划线分隔（`basic_file_ops`、`version_and_help`、`error_handling`）

### 脚本命名

- 入口脚本统一使用 `test.sh`
- 辅助脚本放在包级 `lib.sh` 中

---

## 生成测试 vs 手工测试

本项目大量使用脚本生成测试用例（如 `gen_p0_tests.py` 等）。生成后必须：

1. 通过 `python -m pytest unittests/ -v` 全部检查
2. 手工抽查至少 3 个生成用例的语义正确性
3. 确认 `main.fmf` 的 `test:` 指向正确的脚本路径