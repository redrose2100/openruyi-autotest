# CI CLI 脚本规范

> `.github/scripts/` 目录下的 Python CLI 框架编写与维护规范。

---

## CLI 框架设计

基于**类的命令行框架**，所有 CI 逻辑封装为可复用的 Python 命令。

### 架构原则

- **自动注册**：`CommandRegistry.discover()` 扫描 `commands/*.py`，任何继承 `BaseCommand` 的类自动注册为子命令
- **单一职责**：一个文件 = 一个命令
- **松耦合**：命令之间只通过 JSON Artifact 通信（`requirements.json`、`vm_info.json`、`test_results.json`）
- **生命周期**：`on_start → run → on_finish`，异常统一处理

---

## 目录结构

```
.github/scripts/
├── cli.py                     # 入口：解析参数 → 委托给 core.base.run_cli()
├── __main__.py                # 支持 python3 -m scripts
├── core/                      # 共享基础设施
│   ├── base.py                #   BaseCommand + CommandRegistry
│   ├── logging.py             #   统一日志
│   ├── config.py              #   环境变量 / JSON / GitHub Actions 输出
│   ├── ssh.py                 #   SSH 客户端（ExecResult / SSHClient）
│   ├── cloudpods.py           #   CloudPods API 客户端
│   ├── github.py              #   GitHub REST API 封装
│   └── repo.py                #   仓库相关工具
└── commands/                  # 命令实现
    ├── compute_requirements.py
    ├── launch_qemu_env.py
    ├── run_tests_in_qemu.py
    ├── post_pr_comment.py
    └── cleanup_cloudpods.py
```

---

## 使用方式

```bash
# 列出所有已注册命令
python3 .github/scripts/cli.py --help

# 查看命令参数
python3 .github/scripts/cli.py compute-requirements --help

# 执行命令
python3 .github/scripts/cli.py -v compute-requirements \
  --repo . --changed-files changed.txt --output req.json
```

---

## 添加新命令

在 `commands/` 下新建文件，如 `commands/hello.py`：

```python
from core.base import BaseCommand

class HelloCommand(BaseCommand):
    """命令描述（用于 --help）"""

    @staticmethod
    def name() -> str:
        return "hello"  # 命令行子命令名

    def register_arguments(self, parser):
        parser.add_argument("--name", required=True, help="名字")

    def run(self, args):
        self.logger.info(f"你好, {args.name}!")
        return 0
```

文件保存后自动注册，无需修改任何注册代码。

---

## 日志规范

| 级别 | 场景 |
|------|------|
| `warning` | 默认（不带参数） |
| `info` | `-v`（一次） |
| `debug` | `-vv`（两次），含 traceback |

```python
self.logger.info("操作完成")
self.logger.debug("详细调试信息: %s", detail)
self.logger.warning("警告信息")
```

---

## 异常处理

- `KeyboardInterrupt` → 退出码 130
- 其他所有异常 → 退出码 1
- `-vv` 时打印完整 traceback
- 禁止吞掉异常而不打日志

---

## 配置读取

通过环境变量或 JSON 文件读取配置：

```python
from core.config import get_config

token = get_config("CLOUDPODS_ACCESS_KEY")  # 从环境变量读取
```

凭证**绝不**硬编码在代码中，通过 GitHub Secrets 注入到 CI 环境。ci-pipeline 的两个文件已经创建好了。接下来创建 `tooling/` 规范和更新 `guides/`。Now creating tooling specs.

<｜DSML｜tool_calls>
<｜DSML｜invoke name="create_file">
<｜DSML｜parameter name="content" string="true"># 工具开发规范

> `tools/` 和 `unittests/` 目录下的 Python 代码编写与维护规范。

---

## 规范索引

| 规范 | 说明 | 状态 |
|------|------|------|
| [Python 编码规范](./python-coding.md) | Python 代码风格与类型注解 | 已填写 |
| [CloudPods 工具规范](./cloudpods.md) | CloudPods 集成工具（K8s/服务器创建） | 已填写 |

---

## 概述

本项目的 Python 代码分为两类：

1. **工具层**（`tools/`）：提供给 CI 和开发者使用的 Python 工具，如 CloudPods 集成
2. **测试框架质检**（`unittests/`）：对测试框架自身的单元测试（pytest）

两者的编码标准统一，但用途不同。