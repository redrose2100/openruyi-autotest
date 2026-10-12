# CI/CD 流水线规范

> GitHub Actions 工作流和 CI 脚本的编写与维护规范。

---

## 规范索引

| 规范 | 说明 | 状态 |
|------|------|------|
| [GitHub Actions 工作流](./github-workflows.md) | workflow 组织、触发条件、自托管 Runner | 已填写 |
| [CI CLI 脚本规范](./pipeline-scripts.md) | `.github/scripts/` 命令行框架规范 | 已填写 |

---

## 架构概览

```
.github/
├── workflows/          # GitHub Actions 工作流（YAML）
│   ├── unit-tests.yml          # 单元测试（push/PR 触发）
│   ├── pr-tests-changed.yml    # PR 变更文件检测 + 关联测试
│   ├── functional-tests.yml    # 功能测试（手动触发）
│   ├── commit-lint.yml         # 提交信息格式检查
│   ├── device-test.yml         # 设备测试
│   ├── qemu-test.yml           # QEMU 测试
│   └── pool-provision.yml      # 资源池管理
└── scripts/            # CI CLI（Python 类框架）
    ├── cli.py                  # 统一入口
    ├── core/                   # 共享基础设施
    │   ├── base.py             #   BaseCommand + 自动注册
    │   ├── logging.py          #   统一日志
    │   ├── config.py           #   环境变量/JSON 配置
    │   ├── ssh.py              #   SSH 客户端
    │   ├── cloudpods.py        #   CloudPods API 客户端
    │   ├── github.py           #   GitHub REST API
    │   └── repo.py             #   仓库工具
    └── commands/               # 命令实现（一个文件 = 一个命令）
        ├── compute_requirements.py
        ├── launch_qemu_env.py
        ├── run_tests_in_qemu.py
        ├── post_pr_comment.py
        └── cleanup_cloudpods.py
```

---

## 快速参考

### 禁止事项

- ❌ **禁止修改 CI 流水线文件**：如流水线本身有 bug，创建 Issue 由用户处理
- ❌ 禁止在 workflow YAML 中写复杂逻辑 → 应封装到 `scripts/` 的 Python 命令中
- ❌ 禁止在仓库中硬编码凭证 → 必须使用 GitHub Secrets 注入