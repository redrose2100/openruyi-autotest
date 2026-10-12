# Shell 脚本规范

> 所有测试脚本（`.sh`）必须遵守以下编码规范。

---

## Shebang

```bash
#!/bin/bash
```

- **必须**在文件第一行（UTF-8 BOM 可容忍，但会触发质量检查警告）
- **必须**是 bash（非 sh/ash/dash），因为测试依赖 bash 扩展特性

---

## 语法检查

所有 `.sh` 文件必须通过 `bash -n` 语法检查：

```bash
bash -n test.sh   # 语法检查，不执行
```

`unittests/test_sh_syntax.py` 会自动对所有 `tests/` 下的 `.sh` 文件执行此检查：

```bash
python -m pytest unittests/test_sh_syntax.py -v
```

---

## 库引用

```bash
# ✅ 正确：使用相对路径从包级 lib.sh 加载
. "$(dirname "$0")/../lib.sh"

# ✅ 正确：加载 Beakerlib
. /usr/share/beakerlib/beakerlib.sh || exit 1

# ✅ 正确：加载跨包共享库
. "$(dirname "$0")/../../lib/hw_check.sh"

# ❌ 错误：硬编码绝对路径
. /root/tests/functional/pkgs/coreutils/lib.sh
```

- `unittests/test_sh_syntax.py` 会验证被引用的 `lib.sh` / `hw_check.sh` 路径真实存在

---

## 变量与引号

```bash
# ✅ 正确：变量使用双引号
rlRun "cd $TmpDir" 0 "进入临时目录"

# ✅ 正确：命令替换用 $()
files=$(ls "$TmpDir")

# ❌ 错误：未加引号的变量（含空格时出 bug）
rlRun cd $TmpDir

# ❌ 错误：使用反引号（已废弃）
files=`ls "$TmpDir"`
```

---

## 格式要求

- 缩进：4 空格（不用 Tab）
- 行尾无多余空格
- 文件末尾保留一个空行
- 禁止中文字符出现在代码注释/命令描述之外的可执行代码中
- 乱码/全角字符禁止出现

---

## 可执行位

测试入口脚本（`test:` 指向的脚本）必须在 git 中标记为可执行：

```bash
git update-index --chmod=+x path/to/test.sh
```

> Windows 文件系统无 POSIX exec 位，因此**以 git 记录的 mode 为准**。
> `unittests/test_fmf_metadata.py` 会检查 git 中的可执行位。