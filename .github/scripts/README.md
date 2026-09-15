# CI CLI（.github/scripts）

统一的**基于类的命令行框架**，把 CI 流水线所需的一切封装为可复用命令。
流水线（workflow）只负责调用命令行，具体实现全部收敛在 `scripts` 目录内，方便扩展与维护。

## 快速上手

```bash
# 查看所有已注册命令
python3 .github/scripts/cli.py --help

# 查看某个命令的参数
python3 .github/scripts/cli.py compute-requirements --help

# 执行命令（-v 输出 INFO 日志，-vv 输出 DEBUG 日志，可加 --log-file）
python3 .github/scripts/cli.py -v compute-requirements \
  --repo . --changed-files changed.txt --output req.json
```

> 所有命令共享两个全局参数：`--verbose/-v`（可重复，0=WARNING / 1=INFO / 2=DEBUG）与 `--log-file`。

## 架构

```
.github/scripts/
├── cli.py                     # 入口：解析全局参数，委托给 core.base.main()
├── __main__.py                # 支持 python3 -m scripts
├── core/                      # 公共库（基类 + 基础设施）
│   ├── base.py                #   BaseCommand 基类 + CommandRegistry + 参数解析
│   ├── logging.py             #   统一日志（终端 + 可选的 JSON 日志文件）
│   ├── config.py              #   环境变量 / JSON / GitHub Actions 输出工具
│   ├── ssh.py                 #   统一 SSH 客户端（ExecResult / SSHClient / wait_ssh_ready）
│   ├── cloudpods.py           #   CloudPods API 客户端（建机 / 查询 / 删除）
│   ├── github.py              #   GitHub REST API 封装（PR 评论等）
│   └── repo.py                #   仓库根目录查找、打包、改动文件收集
└── commands/                  # 命令实现：每个 CI 检查一个文件，自动注册
    ├── compute_requirements.py
    ├── launch_qemu_env.py
    ├── run_tests_in_qemu.py
    ├── post_pr_comment.py
    └── cleanup_cloudpods.py
```

## 设计要点

- **自动注册**：`CommandRegistry.discover()` 扫描 `commands/*.py`，凡是继承 `BaseCommand`
  且定义在同文件的类都会被自动注册为子命令，新增命令无需修改任何注册代码。
- **面向对象**：每个命令一个文件，命令之间只通过 JSON 产物（`requirements.json`、
  `vm_info.json`、`test_results.json`）解耦，可独立替换/新增。
- **生命周期**：`on_start → run → on_finish`，任何异常统一收敛（`KeyboardInterrupt → 130`，
  其余 `→ 1`，`-vv` 下打印 traceback）。
- **统一配置**：命令通过环境变量或 JSON 读取配置，凭据不落库（GitHub Actions 中用
  `secrets.*` 注入）。

## 扩展指南：新增一个命令

在 `commands/` 下新建一个文件，例如 `commands/hello.py`：

```python
from core.base import BaseCommand


class HelloWorldCommand(BaseCommand):
    name = "hello-world"
    description = "输出问候语"

    def setup_parser(self, parser):
        parser.add_argument("--who", default="world", help="问候对象")

    def run(self, args):
        self.log_info("Hello, %s!", args.who)
        return 0
```

保存后立即生效，无需注册：

```bash
python3 .github/scripts/cli.py hello-world --who ci
```

## 命令说明

| 命令 | 作用 | 关键输入 | 产物 |
| --- | --- | --- | --- |
| `compute-requirements` | 根据变更的测试文件计算资源规格（CPU/内存/SKU/依赖包） | `--changed-files` | `requirements.json` |
| `launch-qemu-env` | 调用 CloudPods 创建 RISC-V QEMU 环境并等待就绪 | `requirements.json` | `vm_info.json` |
| `run-tests-in-qemu` | 通过 SSH 在远端执行 tmt/BeakerLib 测试并汇总结果 | `vm_info.json` | `test_results.json` |
| `post-pr-comment` | 把测试结果以 Markdown 评论发布到 PR | `test_results.json` | PR 评论 |
| `cleanup-cloudpods` | 销毁本次创建的 CloudPods 服务器，避免残留计费 | `vm_info.json` | — |

## 流水线对接

`pr-tests-changed.yml` 中的执行顺序（每个步骤即一次 CLI 调用）：

```yaml
python3 .github/scripts/cli.py compute-requirements ...   # 1. 计算资源规格
python3 .github/scripts/cli.py launch-qemu-env ...          # 2. 拉起 QEMU 环境
python3 .github/scripts/cli.py run-tests-in-qemu ...        # 3. 执行测试
python3 .github/scripts/cli.py cleanup-cloudpods ...        # 4. 清理环境
```

> 注：流水线不再自动发布 PR 评论（fork 仓库提交的 PR 中 `GITHUB_TOKEN` 为只读，
> 评论 API 会 403 失败）。`post-pr-comment` 命令保留，可用于同仓库 PR 或手动场景。

## 测试

`unittests/test_ci_cli.py` 覆盖：命令自动发现、基类约定、`compute-requirements`
的规格计算、PR 评论的 Markdown 生成等。本地运行：

```bash
python -m pytest unittests/test_ci_cli.py -q
```
