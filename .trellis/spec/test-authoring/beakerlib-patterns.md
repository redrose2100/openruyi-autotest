# Beakerlib 测试模式

> 本项目所有功能测试使用 Beakerlib 作为测试框架，必须遵守以下模式。

---

## 生命周期：三阶段必须完整

每个 `test.sh` 必须是 **Setup → Test → Cleanup** 三阶段结构：

```bash
#!/bin/bash
# Functional test: <包名> - <功能描述>

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    <包名>Setup                          # 调用包级 lib.sh 中的初始化函数
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    # 按需创建测试文件
    rlPhaseEnd

    rlPhaseStartTest "<功能描述>"
    rlRun "<测试命令>" <期望退出码> "<描述>"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
```

### 强制规则

- ✅ 每个 `test.sh` **必须**包含 `rlJournalStart` / `rlJournalEnd`
- ✅ 每个 `test.sh` **必须**包含 `rlPhaseStartSetup` / `rlPhaseStartTest` / `rlPhaseStartCleanup`
- ✅ `rlPhaseStartSetup` 中**必须**调用包级 `Setup` 函数（如 `coreutilsSetup`）
- ✅ rlPhaseStartCleanup 中**必须**清理临时目录
- ❌ 禁止省略 rlPhaseEnd 匹配
- ❌ 禁止在 rlPhaseStartTest 之前缺少 rlPhaseStartSetup

---

## rlRun 规范

```bash
rlRun "<命令>" <期望退出码> "<描述>"
```

### 规则

- 退出码：`0` = 期望成功，`1` = 期望失败
- 描述必须简洁描述**在测什么**，不是"执行某命令"
  - ✅ `"验证 b2sum 正确输出 BLAKE2 校验和"`
  - ❌ `"执行 b2sum file1.txt"`
- 每个功能点至少一个正向测试（exit=0），推荐补充错误路径测试

### 错误处理模式

```bash
# ✅ 正确：命令失败时用 || true 容错，单独检查
rlRun "cmd 2>&1" 0 "执行 cmd 进行后续检查"

# ❌ 错误：不要用 grep 管道包装来"捕捉"错误
rlRun "cmd 2>&1 | grep -qiE 'error|Error'" 0 "检查错误"
```

---

## 包级 lib.sh

每个包目录下的 `lib.sh` 提供共享初始化函数：

```bash
# lib.sh — <包名> 共享函数
<包名>Setup() {
    rlRun "rpm -q <包名>" 0 "验证 <包名> 已安装"
}
```

- 函数命名：`<小写包名>Setup`（如 `coreutilsSetup`、`curlSetup`）
- 引用方式：`test.sh` 中用 `. "$(dirname "$0")/../lib.sh"` 加载