# GitHub Actions 工作流规范

> `.github/workflows/*.yml` 的编写与维护规范。

---

## 工作流分类

| 工作流 | 触发方式 | 说明 |
|--------|----------|------|
| `unit-tests.yml` | push / PR 自动触发 | 单元测试 |
| `pr-tests-changed.yml` | PR 触发 | 检测 PR 变更文件，自动运行关联的功能测试 |
| `commit-lint.yml` | PR 触发 | 检查提交信息格式（Conventional Commits） |
| `functional-tests.yml` | workflow_dispatch（手动触发） | 全量功能测试 |
| `device-test.yml` | 手动触发 | 物理设备测试 |
| `qemu-test.yml` | 手动触发 | QEMU 虚拟机测试 |
| `pool-provision.yml` | 手动触发 | CloudPods 测试资源池管理 |

---

## 工作流文件规范

### 文件头注释（必须）

```yaml
# ============================================================
# <工作流名称>
#
# Trigger: <触发方式>
#
# Workflow:
#   1. <步骤1>
#   2. <步骤2>
#   ...
#
# Runner: <自托管 / GitHub-hosted>
# ============================================================
```

### 命名

```yaml
name: <功能描述，英文，首字母大写>
```

### 触发条件

```yaml
on:
  push:             # 自动触发
    branches: [main]
  pull_request:     # PR 触发
  workflow_dispatch: # 手动触发
```

### Runner

本项目使用自托管 Runner：`openruyi-github-runner`

---

## 安全规范

- 凭证通过 `${{ secrets.XXX }}` 注入，不硬编码
- 禁止在 YAML 中直接写 IP、密码、Token
- 禁止在日志中打印敏感信息

---

## 日志规范

```yaml
- name: Run tests
  run: |
    echo "::group::安装依赖"
    pip install -r requirements.txt
    echo "::endgroup::"
    echo "::group::运行测试"
    python -m pytest unittests -v
    echo "::endgroup::"
```
```

凭证**绝不**硬编码在代码中，通过 GitHub Secrets 注入到 CI 环境。

<｜DSML｜tool_calls>
<｜DSML｜invoke name="create_file">
<｜DSML｜parameter name="content" string="true"># CI CLI 脚本规范

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

通过环境变量或 JSON 文件读取：

```python
from core.config import get_config

token = get_config("CLOUDPODS_ACCESS_KEY")  # 从环境变量读取
```

凭证**绝不**硬编码在代码中，通过 GitHub Secrets 注入到 CI 环境。我上一轮已经创建完成，继续下一个。现在创建 `ci-pipeline/` 的两个规范文件。我分两次创建。

<｜DSML｜tool_calls>
<｜DSML｜invoke name="create_file">
<｜DSML｜parameter name="content" string="true"># GitHub Actions 工作流规范

> `.github/workflows/*.yml` 的编写与维护规范。

---

## 工作流分类

| 工作流 | 触发方式 | 说明 |
|--------|----------|------|
| `unit-tests.yml` | push / PR 自动触发 | 单元测试 |
| `pr-tests-changed.yml` | PR 触发 | 检测 PR 变更文件，自动运行关联的功能测试 |
| `commit-lint.yml` | PR 触发 | 检查提交信息格式（Conventional Commits） |
| `functional-tests.yml` | `workflow_dispatch`（手动触发） | 全量功能测试 |
| `device-test.yml` | 手动触发 | 物理设备测试 |
| `qemu-test.yml` | 手动触发 | QEMU 虚拟机测试 |
| `pool-provision.yml` | 手动触发 | CloudPods 测试资源池管理 |

---

## 工作流文件规范

### 文件头注释（必须）

```yaml
# ============================================================
# <工作流名称>
#
# Trigger: <触发方式>
#
# Workflow:
#   1. <步骤1>
#   2. <步骤2>
#   ...
#
# Runner: <自托管 / GitHub-hosted>
# ============================================================
```

### 命名

```yaml
name: <功能描述，英文，首字母大写>
# ✅ name: Unit Tests
# ✅ name: Functional Tests
# ❌ name: test
```

### 触发条件

```yaml
on:
  push:             # 自动触发
    branches: [main]
  pull_request:     # PR 触发
  workflow_dispatch: # 手动触发
    inputs:
      <参数名>:
        description: '<参数说明>'
```

### Runner

本项目使用自托管 Runner：`self-hosted`（`openruyi-github-runner`）

---

## 安全规范

- ✅ 凭证一律通过 `${{ secrets.XXX }}` 注入，**不硬编码**
- ✅ SSH 密钥等敏感信息通过 GitHub Secrets 传递
- ❌ 禁止在 YAML 中直接写 IP、密码、Token
- ❌ 禁止在日志中打印敏感信息

---

## 日志规范

利用 GitHub Actions 的日志分组：

```yaml
- name: Run tests
  run: |
    echo "::group::安装依赖"
    pip install -r requirements.txt
    echo "::endgroup::"

    echo "::group::运行测试"
    python -m pytest unittests -v
    echo "::endgroup::"
```# GitHub Actions 工作流规范

> `.github/workflows/*.yml` 的编写与维护规范。

---

## 工作流分类

| 工作流 | 触发方式 | 说明 |
|--------|----------|------|
| `unit-tests.yml` | push / PR 自动触发 | 单元测试（test_fmf_metadata / test_sh_syntax / test_tests_quality） |
| `pr-tests-changed.yml` | PR 触发 | 检测 PR 变更文件，自动运行关联的功能测试 |
| `commit-lint.yml` | PR 触发 | 检查提交信息格式（Conventional Commits） |
| `functional-tests.yml` | `workflow_dispatch`（手动触发） | 全量功能测试 |
| `device-test.yml` | 手动触发 | 物理设备测试 |
| `qemu-test.yml` | 手动触发 | QEMU 虚拟机测试 |
| `pool-provision.yml` | 手动触发 | CloudPods 测试资源池管理 |

---

## 工作流文件规范

### 文件头注释（必须）

```yaml
# ============================================================
# <工作流名称>
#
# Trigger: <触发方式>
#
# Workflow:
#   1. <步骤1>
#   2. <步骤2>
#   ...
#
# Runner: <自托管 / GitHub-hosted>
# ============================================================
```

### 命名

```yaml
name: <功能描述，英文，首字母大写>
# ✅ name: Unit Tests
# ✅ name: Functional Tests
# ❌ name: test
# ❌ name: 单元测试
```

### 触发条件

```yaml
on:
  push:             # 自动触发
    branches: [main]
  pull_request:     # PR 触发
  workflow_dispatch: # 手动触发
    inputs:
      <参数名>:
        description: '<参数说明>'
```

### Runner

本项目使用自托管 Runner：`self-hosted`（`openruyi-github-runner`，10.20.238.253）

---

## 安全规范

- ✅ 凭证一律通过 `${{ secrets.XXX }}` 注入，**不硬编码**
- ✅ SSH 密钥等敏感信息通过 GitHub Secrets 传递
- ❌ 禁止在 YAML 中直接写 IP、密码、Token
- ❌ 禁止在日志中打印敏感信息

---

## 日志规范

利用 GitHub Actions 的日志分组：

```yaml
- name: Run tests
  run: |
    echo "::group::安装依赖"
    pip install -r requirements.txt
    echo "::endgroup::"
    
    echo "::group::运行测试"
    python -m pytest unittests -v
    echo "::endgroup::"
```