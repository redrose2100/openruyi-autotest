# CI 指南

本文档介绍 openruyi-autotest 中使用的 CI/CD 工作流和检查点，包括 CI 预置池架构和测试执行流水线。

---

## 1. 概述

```mermaid
flowchart TB
    subgraph "每次推送 / PR"
        A[Git 推送 / PR] --> B[提交信息检查]
        A --> C[单元测试]
    end

    subgraph "PR 合入 main（tests/ 有改动）"
        D[PR 合入 main] --> E[检测变更文件]
        E --> F[计算 VM 资源需求]
        F --> G[从 CI 池申请环境]
        G --> H[在 QEMU 中运行测试]
        H --> I[释放环境回池]
    end

    subgraph "后台定时（每 30 分钟）"
        J[池定时补齐] --> K[检查镜像哈希]
        K --> L[补齐/修复池]
    end

    B --> M{通过？}
    C --> M
    M -->|是| N[可合并]
    M -->|否| O[阻止合并]
```

| 工作流 | 触发条件 | 运行器 | 说明 |
|----------|---------|--------|-------------|
| **提交信息检查** | 每次推送 / PR | `ubuntu-latest` | 验证提交信息符合 [约定式提交](commit_guide_zh.md) |
| **单元测试** | 每次推送 / PR | `ubuntu-latest` | fmf 元数据、CI CLI 逻辑、Shell 语法、文档检查 |
| **PR 测试变更验证** | PR 合入 `main` 且 `tests/` 有改动 | `self-hosted` | 检测变更测试，从 CI 预置池获取 VM，在 QEMU 中执行测试，释放回池 |
| **CI 预置池补齐** | 定时（每 30 分钟）/ 手动 | `self-hosted` | 幂等填补双池至目标容量 |
| **Functional 全量测试** | 手动触发 | `self-hosted` | 全量 functional 测试套（281 套） |
| **QEMU RISC-V 测试** | 手动触发 | `self-hosted` | RISC-V QEMU 仿真测试 |
| **物理设备测试** | 手动触发 | `self-hosted` | RISC-V 真机测试 |

---

## 2. 自动运行的工作流

### 2.1 提交信息检查

**触发条件：** 任意分支的 `push` 和 `pull_request`。

```mermaid
flowchart LR
    A[触发: push / PR] --> B[检出代码]
    B --> C[计算 commit 范围]
    C --> D[执行 commit-lint.sh]
    D --> E{格式检查}
    E -->|通过| F[✅ 成功]
    E -->|失败| G[❌ 阻止]
```

**检查点：**

| # | 规则 | 示例（✅ 正确） | 示例（❌ 错误） |
|---|------|---------------------|-------------------|
| 1 | 格式：`<type>(<scope>): <summary>` | `fix(ci): support format args` | `fixed ci bug` |
| 2 | 仅限 ASCII 英文 | `feat: add new test` | `feat: 添加新测试` |
| 3 | 摘要以小写字母开头 | `fix: correct assertion` | `fix: Correct assertion` |
| 4 | 摘要 ≤ 72 字符 | `chore: update deps` | `chore: update dependencies to the latest version available` |
| 5 | 不以句号结尾 | `docs: add guide` | `docs: add guide.` |

> 完整规范参见 [提交指南](commit_guide_zh.md)。

### 2.2 单元测试

**触发条件：** 任意分支的 `push` 和 `pull_request`。

```mermaid
flowchart LR
    A[触发: push / PR] --> B[检出代码]
    B --> C[Python 3.11 环境]
    C --> D[安装 pytest / pyyaml]
    D --> E{并行 Job}
    E --> F1[Quick: fmf 元数据]
    E --> F2[CI CLI: 命令 + 逻辑]
    E --> F3[Docs: 不暴露 openEuler]
    E --> F4[Shell: 语法检查]
    E --> F5[Lib: 逻辑测试]
    E --> F6[Tests: 质量检查]
    F1 --> G{汇总}
    F2 --> G
    F3 --> G
    F4 --> G
    F5 --> G
    F6 --> G
    G -->|全部通过| H[✅ 成功]
    G -->|任一失败| I[❌ 阻止]
```

**检查点：**

| Job | 检查内容 |
|-----|---------------|
| `quick` | FMF 元数据正确性（`.fmf/version`、plans、测试结构） |
| `ci-cli` | CI CLI 命令注册、参数解析、cloudpods/ssh/github 模块 |
| `docs-lint` | `docs/` 中无不出现 `openEuler`（合规要求） |
| `shell-syntax` | 所有 `.sh` 脚本语法检查（bash -n） |
| `lib-logic` | `tests/lib/` 辅助函数逻辑 |
| `tests-quality` | 测试用例质量：BeakerLib `rlJournalPrintText` 使用、元数据完整性 |

---

## 3. PR 测试变更验证

这是 PR 审查的核心 CI 流水线。**仅当** PR 目标为 `main` 且 `tests/` 下有变更时运行。

```mermaid
flowchart TB
    subgraph "触发"
        PR[PR 合入 main] --> CHECK{tests/ 有改动?}
        CHECK -->|否| SKIP[⏭️ 跳过]
        CHECK -->|是| STEP1
    end

    subgraph "步骤 1：检测"
        STEP1[获取变更文件] --> DIFF[git diff --name-only]
        DIFF --> LIST[changed_files.txt]
    end

    subgraph "步骤 2：需求计算"
        LIST --> COMPUTE[compute-requirements]
        COMPUTE --> REQ[vm_requirements.json]
    end

    subgraph "步骤 3：池申请"
        REQ --> ACQUIRE[pool-acquire]
        ACQUIRE --> |server_count=1| POOLA[池 A: 1q × 20]
        ACQUIRE --> |server_count=2| POOLB[池 B: 2q × 5]
        POOLA --> VM[vm_info.json]
        POOLB --> VM
    end

    subgraph "步骤 4：执行测试"
        VM --> QEMU[run-tests-in-qemu]
        QEMU --> RESULT[test_results.json]
    end

    subgraph "步骤 5：清理"
        RESULT --> RELEASE[pool-release]
        RELEASE --> DONE[✅ 完成]
    end
```

**检查点：**

| 检查点 | 验证内容 |
|-----------|------------------|
| `changed_files.txt` | 文件列表非空；路径均在 `tests/` 下 |
| `vm_requirements.json` | `server_count`（1 或 2）、`packages`、`reason` |
| 池申请 | 600s 超时内 SSH 可达；生成有效的 `vm_info.json`（含 host_ip + qemu_ports） |
| 测试执行 | 所有 BeakerLib 测试脚本返回通过/失败；生成 `test_results.json` |
| 池释放 | VM 归还池中（不删除）；`pool-release` 总是执行（`if: always()`） |

### 3.1 CI 预置池架构

```mermaid
flowchart LR
    subgraph "池 A（1 QEMU × 20）"
        A1[VM-1q-01]
        A2[VM-1q-02]
        A3[...]
        A20[VM-1q-20]
    end

    subgraph "池 B（2 QEMU × 5）"
        B1[VM-2q-01]
        B2[VM-2q-02]
        B3[...]
        B5[VM-2q-05]
    end

    ACQ[pool-acquire] -->|server_count=1| A1
    ACQ -->|server_count=2| B1

    REL[pool-release] -->|归还| A1
    REL -->|归还| B1

    PROV[pool-provision] -->|补齐| A1
    PROV -->|补齐| B1
```

| 池 | 规格 | 每 VM QEMU 数 | 最大数量 | 前缀 |
|------|-----|------------|-----------|--------|
| A | `ecs.g1.c8m8` | 1 | 20 | `openruyi-ci-pool-1q` |
| B | `ecs.g1.c16m16` | 2 | 5 | `openruyi-ci-pool-2q` |

**池行为：**

- **镜像哈希检查：** 预置前比较当前 CloudPods 镜像哈希与存储的哈希。若不匹配 → 删除所有池 VM 并重建。
- **定时补齐：** 每 30 分钟幂等地将双池填补至目标容量。
- **申请：** 查找健康的 VM（SSH 可达），预留它，返回 `vm_info.json`。
- **释放：** 将 VM 归还池中（SSH 探测确认仍健康）。
- **双池路由：** `server_count=1` → 池 A；`server_count=2` → 池 B。

---

## 4. 手动触发的工作流

### 4.1 Functional 全量测试

```mermaid
flowchart LR
    A[手动触发] --> B[检出代码]
    B --> C[安装依赖]
    C --> D[运行全量功能测试]
    D --> E[上传报告]
    E --> F[制品: reports/]
```

**参数：** `suite`（逗号分隔，留空=全部），`no_cleanup`（保留 VM 用于调试）。

### 4.2 QEMU RISC-V 测试

```mermaid
flowchart LR
    A[手动触发] --> B[检出代码]
    B --> C[安装工具]
    C --> D[下载镜像 + 固件]
    D --> E[扩容镜像（< 2G 时）]
    E --> F[启动 QEMU（screen 会话）]
    F --> G[等待 SSH 就绪]
    G --> H[通过 run-tests action 执行]
    H --> I[上传结果]
```

### 4.3 物理设备测试

```mermaid
flowchart LR
    A[手动触发] --> B[检出代码]
    B --> C[安装工具]
    C --> D[从 secrets 读取 DEVICE_IP]
    D --> E[在物理设备上执行测试]
    E --> F[上传结果]
```

---

## 5. CI 预置池补齐（后台定时）

```mermaid
flowchart TB
    CRON[定时: */30 * * * *] --> CHECKOUT[检出代码]
    MANUAL[手动: workflow_dispatch] --> CHECKOUT
    CHECKOUT --> DEPS[安装 paramiko]
    DEPS --> HASH{镜像哈希变更？}
    HASH -->|是| REBUILD[删除所有池 VM<br>全部重建]
    HASH -->|否| FILL[探测各池<br>补齐缺失 VM]
    REBUILD --> STATUS[pool-status 报告]
    FILL --> STATUS
    STATUS --> DONE[✅ 完成]
```

**检查点：**

| 检查点 | 动作 |
|-----------|--------|
| 镜像哈希不匹配 | 删除所有现有池 VM → 完全重建 |
| 池 A < 20 | 使用 SKU `ecs.g1.c8m8` 创建缺失 VM |
| 池 B < 5 | 使用 SKU `ecs.g1.c16m16` 创建缺失 VM |
| SSH 探测 | 标记为健康前检查每个 VM 的可达性 |

---

## 6. CI 脚本架构

```mermaid
flowchart TB
    subgraph "入口"
        CLI[cli.py]
    end

    subgraph "核心模块"
        BASE[core/base.py<br>BaseCommand]
        CP[core/cloudpods.py<br>CloudPods API]
        SSH[core/ssh.py<br>SSH 工具]
        GH[core/github.py<br>GitHub API]
        REPO[core/repo.py<br>仓库操作]
        LOG[core/logging.py<br>日志配置]
    end

    subgraph "命令"
        CREQ[compute-requirements]
        PACQ[pool-acquire]
        PREL[pool-release]
        PPROV[pool-provision]
        PSTAT[pool-status]
        RTQ[run-tests-in-qemu]
        LQE[launch-qemu-env]
        CLP[cleanup-cloudpods]
        PPR[post-pr-comment]
    end

    subgraph "池模块"
        POOLC[pool/core.py<br>CIPool 类]
        POOLI[pool/__init__.py]
    end

    CLI --> BASE
    CLI --> CREQ & PACQ & PREL & PPROV & PSTAT & RTQ & LQE & CLP & PPR
    PACQ --> POOLC
    PREL --> POOLC
    PPROV --> POOLC
    PSTAT --> POOLC
    POOLC --> CP
    POOLC --> SSH
    BASE --> LOG
```

| 模块 | 作用 |
|--------|------|
| `cli.py` | 主 CLI 入口；通过 `CommandRegistry` 注册所有命令 |
| `core/base.py` | `BaseCommand`，含 `log_info`/`log_warn`/`log_error`、参数解析、`execute()` |
| `core/cloudpods.py` | CloudPods REST API 封装（`launch_env`、`delete_server`、`list_servers` 等） |
| `core/ssh.py` | SSH 连接、文件传输、远程执行 |
| `core/github.py` | GitHub API 封装（PR 信息、评论、checks） |
| `core/repo.py` | 仓库操作（tarball 打包、路径解析） |
| `pool/core.py` | `CIPool` 类，含 `acquire`/`release`/`delete_all`/`probe_all` |

---

## 7. 快速参考

### PR 工作流检查点

| 步骤 | 检查内容 | 通过条件 |
|------|-------|---------------|
| 提交检查 | 格式、ASCII、小写、长度 | 范围内全部 commit 通过 |
| 单元测试 | 6 个并行 job | 全部 6 个通过 |
| 变更文件 | `tests/` 下的 `git diff` | 非空 → 继续 |
| VM 需求 | `compute-requirements` 输出 | 有效 JSON，含 `server_count` |
| 池申请 | `pool-acquire --timeout 600` | 超时内 SSH 可达 |
| 测试执行 | `run-tests-in-qemu` | 全部测试脚本通过 |
| 池释放 | `pool-release`（总是执行） | VM 归还池中 |

### 常见问题

| 现象 | 可能原因 | 处理方式 |
|---------|-------------|--------|
| 提交检查失败 | 非 ASCII 或格式错误 | 按[提交指南](commit_guide_zh.md)修改 commit message |
| 池申请超时 | 池已空或 VM 不可达 | 手动触发 `pool-provision` 或等待定时任务 |
| 测试执行失败 | 测试脚本 bug | 查看 workflow 制品中的 `run_tests.log` |
| Job 卡在排队 | 自托管运行器离线 | 检查 `10.20.238.253` 上的 runner 状态 |