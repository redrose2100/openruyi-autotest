# FMF 元数据规范

> TMT (Test Management Tool) 使用 `main.fmf` 文件描述测试用例的元数据。
> 本文档定义本项目中 `main.fmf` 的字段约定。

---

## 层级继承

```
tests/
├── main.fmf              # 全局共享配置（所有子目录继承）
└── functional/
    ├── main.fmf           # functional 层共享配置
    └── pkgs/
        ├── main.fmf       # pkgs 层共享配置
        └── coreutils/
            ├── main.fmf   # 包级配置（按需覆盖）
            └── test_coreutils_xxx/
                └── main.fmf  # 用例级（test: 字段在此）
```

- **分组目录**（如 `smoke/`、`functional/pkgs/`、`compatibility/ltp_posix/aio/`）的 `main.fmf` 只提供继承配置，**不包含** `test:` 字段
- **用例目录**必须包含 `test:` 字段指向可执行脚本

---

## 必填字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `summary` | string | 测试用例一句话描述 | `"Coreutils basic file operations test"` |
| `test` | string | 测试入口脚本（相对路径） | `"test.sh"` 或 `"runtest.sh"` |
| `duration` | string | 预估执行时间 | `"5m"`, `"1h"`, `"30s"` |
| `tier` | int | 测试等级 | `0` / `1` / `2` |
| `tag` | list/string | 标签（用于筛选/分组） | `[functional, coreutils]` |
| `path` | string | 测试执行路径（从 tests/ 开始） | `"/tests/functional/pkgs/coreutils"` |

### tier 等级定义

| tier | 含义 | 运行频率 |
|------|------|----------|
| 0 | 冒烟测试 | 每次提交 |
| 1 | 核心/安全测试 | 每日构建 |
| 2 | 兼容性/性能/可靠性测试 | 发布前 |

### duration 格式

`数字 + 单位`：`s`（秒）、`m`（分钟）、`h`（小时）、`d`（天）

---

## 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `contact` | string | 负责人/团队 |
| `require` | list | 依赖包（如 `[beakerlib, coreutils]`） |
| `enabled` | bool | 是否启用（默认 true） |
| `framework` | string | 测试框架（默认 `shell`） |
| `extra-hardware-require` | dict | 硬件要求（`server`, `cpu`, `memory`, `disk`, `net`） |

---

## 验证方式

`unittests/test_fmf_metadata.py` 自动校验：
- 每个 `main.fmf` 是合法 YAML 且顶层为 mapping
- 必填字段存在且类型正确（`duration` 必须匹配 `\d+[smhd]$`，`tier` 必须是 0-2 的整数）
- `test:` 指向的脚本存在且为可执行文件（以 git mode 为准）
- 脚本开头为 `#!/bin/bash`（容忍 BOM）

运行：`python -m pytest unittests/test_fmf_metadata.py -v`