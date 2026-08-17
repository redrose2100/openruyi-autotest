# 用户指南

> 适用于**干净服务器**环境，从零开始执行测试。

> :us: [English Version (英文版)](user_guide.md)

---

## 1. 环境准备

### 1.1 安装 git

```bash
sudo dnf install -y git
```

### 1.2 克隆代码仓库

```bash
git clone https://git.openruyi.cn/woqidaideshi/openruyi-autotest.git
cd openruyi-autotest
```

### 1.3 安装 tmt 和 beakerlib

测试用例使用 tmt (Test Management Tool) 框架管理和执行：

```bash
# 安装 tmt（基础版，支持本地执行）
sudo dnf install -y tmt

# 安装 beakerlib 测试框架
sudo dnf install -y beakerlib

# beakerlib 运行时依赖
sudo dnf install -y python-six

# 验证安装
tmt --version
rpm -q beakerlib
```

> **riscv64 架构**：`tmt` 可能不在 dnf 仓库中，可通过 pip 安装：
> ```bash
> sudo dnf install -y python3 python3-pip rust gcc gcc-c++ beakerlib
> sudo pip3 install --break-system-packages tmt
> ```

### 1.4 配置测试拓扑（可选）

测试计划会自动检测当前机器硬件资源（CPU/内存/磁盘/网卡）是否满足测试用例的硬件需求。如需在多台服务器上执行测试，或者自定义服务器连接信息，可配置 `topology.env`：

```bash
# 复制模板
cp topology.env.example topology.env

# 按实际环境修改
vim topology.env
```

**配置变量说明：**

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TEST_SERVER_COUNT` | 可用服务器数量 | 1 |
| `TEST_SERVER_1_HOST` | 第 1 台服务器 IP/主机名 | (无) |
| `TEST_SERVER_1_PORT` | 第 1 台服务器 SSH 端口 | 22 |
| `TEST_SERVER_1_USER` | 第 1 台服务器登录用户名 | root |
| `TEST_SERVER_1_PASSWORD` | 第 1 台服务器登录密码 | (无) |

多服务器示例（3 台）：

```ini
TEST_SERVER_COUNT=3

TEST_SERVER_1_HOST=192.168.1.10
TEST_SERVER_1_PORT=22
TEST_SERVER_1_USER=root
TEST_SERVER_1_PASSWORD=mypassword

TEST_SERVER_2_HOST=192.168.1.11
TEST_SERVER_2_PORT=12055
TEST_SERVER_2_USER=openruyi
TEST_SERVER_2_PASSWORD=mypassword

TEST_SERVER_3_HOST=192.168.1.12
TEST_SERVER_3_USER=root
# 端口/密码未设置时使用默认值 22 / 无密码
```

> **未配置 `topology.env` 不影响单机测试**。系统将当前机器视为唯一服务器（`TEST_SERVER_COUNT` 默认为 1），硬件资源通过系统命令自动获取。

---

## 2. 执行单个测试用例

比如 acl 测试套中的 `test_acl_getfacl_basic`：

```bash
cd openruyi-autotest

tmt run --all --verbose plan --name /plans/functional \
    test --name /tests/functional/pkgs/acl/test_acl_getfacl_basic \
    provision --feeling-safe
```

> **关于 `--feeling-safe`**：tmt 默认会询问用户确认后才执行，加上此参数跳过交互式确认，适合自动化/无人值守场景。

---

## 3. 执行单个测试套

比如 acl：

```bash
cd openruyi-autotest

tmt run --all plan --name /plans/functional \
    test --name /tests/functional/pkgs/acl \
    provision --feeling-safe
```

---

## 4. 执行测试类型全量用例

比如功能测试（functional），包含 202 个软件包，共 566 个测试用例：

```bash
cd openruyi-autotest

tmt run --all plan --name /plans/functional \
    provision --feeling-safe
```

比如特性测试（feature）：

```bash
tmt run --all plan --name /plans/feature \
    provision --feeling-safe
```

---

## 5. 查看测试结果和日志

### 5.1 tmt 结果目录

tmt 每次执行都会在 `/var/tmp/tmt/run-*` 下生成一个运行目录，包含所有测试用例的详细日志：

```bash
# 列出所有历史运行
ls -lt /var/tmp/tmt/

# 进入最近一次运行目录
cd $(ls -dt /var/tmp/tmt/run-* | head -1)
```

运行目录结构：

```
/var/tmp/tmt/run-XXX/
├── plans/
│   └── {plan-name}/            # 如 functional
│       └── execute/
│           └── data/
│               └── guest/      # 本地执行时为 guest
│                   └── default-0/
│                       └── tests/functional/pkgs/acl/
│                           ├── test_acl_getfacl_basic-1/
│                           │   └── output.txt    # 该用例的完整输出
│                           ├── test_acl_setfacl_basic-2/
│                           │   └── output.txt
│                           └── ...
└── run.yaml                    # 运行元数据
```

### 5.2 查看单个用例日志

```bash
# 进入最近一次运行目录
RUN_DIR=$(ls -dt /var/tmp/tmt/run-* | head -1)

# 路径包含 plans/ 和 guest/default-0/ 层级
BASE="$RUN_DIR/plans/functional/execute/data/guest/default-0"

# 查看某个测试用例的完整输出
cat "$BASE/tests/functional/pkgs/acl/test_acl_getfacl_basic-1/output.txt"
```

### 5.3 查看汇总报告

```bash
# 简要报告
tmt run --last report

# 详细报告（含每个用例的 stdout/stderr）
tmt run --last report -fvvv
```

### 5.4 查看所有用例的执行状态

```bash
RUN_DIR=$(ls -dt /var/tmp/tmt/run-* | head -1)
BASE="$RUN_DIR/plans/functional/execute/data/guest/default-0"

# 列出所有用例的 output.txt 并显示最后几行（通常包含 PASS/FAIL）
find "$BASE" -name "output.txt" | sort | while read f; do
    dir=$(dirname "$f")
    echo "=== $(basename "$dir") ==="
    tail -5 "$f"
    echo ""
done
```

---

## 6. 执行所有测试脚本

从项目根目录执行全部测试（所有计划）：

```bash
cd openruyi-autotest

tmt run --all provision --how local --feeling-safe
```

---

## 7. 目录结构速查

```
tests/
├── smoke/             # 冒烟测试（100 个用例）
│   ├── archive/       # 归档工具（tar, gzip, xz）
│   ├── dev_tools/     # 开发工具
│   ├── disk_fs/       # 磁盘/文件系统
│   ├── filesystem/    # 文件系统操作
│   ├── kernel/        # 内核功能
│   ├── logging/       # 日志系统
│   ├── network/       # 网络工具
│   ├── package_mgmt/  # 包管理
│   ├── permissions/   # 权限管理
│   ├── process/       # 进程管理
│   ├── scripting/     # 脚本语言
│   ├── security/      # 安全相关
│   ├── service_mgmt/  # 服务管理
│   ├── shell_basics/  # Shell 基础
│   ├── system_info/   # 系统信息
│   ├── text_processing/# 文本处理
│   └── user_mgmt/     # 用户管理
├── functional/pkgs/   # 功能测试（202 个包, 566 用例）
│   ├── acl/           # ACL 权限管理（参考标准）
│   ├── attr/          # 扩展属性
│   ├── bash/          # Bash shell
│   ├── coreutils/     # 核心工具集
│   ├── ...            # 更多软件包
├── security/          # 安全测试（106 个用例）
│   ├── cve/           # CVE 漏洞验证
│   └── nmap/          # Nmap 端口扫描
├── compatibility/     # 兼容性测试（188 个用例）
│   └── ltp_posix/     # LTP POSIX 接口兼容性
├── performance/       # 性能测试
│   └── unixbench/     # UnixBench 基准测试
├── feature/           # 特性测试
│   └── <xxx>/         # 特性名称
└── reliability/       # 可靠性测试
    └── test.sh
```

---

## 8. 常见问题

### Q: 执行报错 `beakerlib.sh: No such file or directory`

```bash
sudo dnf install -y beakerlib
```

### Q: tmt 命令找不到

```bash
# dnf 安装
sudo dnf install -y tmt

# 或 pip 安装（riscv64）
sudo pip3 install --break-system-packages tmt
```

### Q: 测试因权限不足失败

部分测试脚本使用 `sudo` 执行特权操作，需确保当前用户有 sudo 权限：

```bash
# 验证 sudo 可用
sudo whoami
```

### Q: 只想查看某个计划包含哪些测试（不执行）

```bash
tmt plan show /plans/functional
tmt test ls /tests/functional/pkgs/acl
```

### Q: 查看上次执行的详细信息

```bash
tmt run --last report -fvvv
```

> **注意**：`tmt run --last report` 有时会因 tmt 内部轮询历史数据而较慢。如果只是查看结果摘要，可以直接读取 `run.yaml` 或查看各用例的 `output.txt`。

### Q: 执行 tmt run 时报 `Synchronization lock ... is stale`

```bash
# 清理旧的 tmt 锁文件（通常由 root 拥有的旧运行残留）
sudo rm -f /var/tmp/tmt-test.pid.lock
```

---

## 9. 实战示例：ACL 测试套

本节以 `acl` 测试套为例，完整展示从环境准备到查看结果的全流程。

### 9.1 前提条件

- 一台干净的 openRuyi 服务器（本示例：10.20.237.192:12055）
- 已安装 git、tmt、beakerlib（参考第 1 节）

### 9.2 克隆仓库并安装依赖

```bash
git clone https://git.openruyi.cn/woqidaideshi/openruyi-autotest.git
cd openruyi-autotest

# 安装 tmt 和测试依赖
sudo dnf install -y tmt beakerlib python-six
sudo dnf install -y acl         # ACL 测试目标软件包
```

### 9.3 （可选）配置 topology.env

```bash
cp topology.env.example topology.env
vim topology.env
```

写入内容：

```ini
TEST_SERVER_COUNT=1
TEST_SERVER_1_HOST=10.20.237.192
TEST_SERVER_1_PORT=12055
TEST_SERVER_1_USER=openruyi
TEST_SERVER_1_PASSWORD=openruyi
```

> 如果当前用户就是 `openruyi` 且在本机执行，可以不配置 `topology.env`，tmt 会自动检测。

### 9.4 清理锁文件（重要）

如果之前执行过 tmt 但异常中断，锁文件可能残留：

```bash
sudo rm -f /var/tmp/tmt-test.pid.lock
```

### 9.5 执行 ACL 测试套

```bash
cd ~/openruyi-autotest

tmt run --all plan --name /plans/functional \
    test --name /tests/functional/pkgs/acl \
    provision --feeling-safe
```

**命令解析：**

| 参数 | 含义 |
|------|------|
| `--all` | 跳过交互确认（和 `--feeling-safe` 配合使用） |
| `plan --name /plans/functional` | 使用功能测试计划（定义在 `plans/functional.fmf`） |
| `test --name /tests/functional/pkgs/acl` | 只执行 `tests/functional/pkgs/acl/` 下的用例 |
| `provision --feeling-safe` | 本地执行，跳过确认 |

**预期输出关键行：**

```
Found 1 plan.
summary: 功能测试 - 验证所有功能测试用例
discover
    how: fmf
    directory: /home/openruyi/openruyi-autotest/tests/functional/pkgs/acl
    filter: tag:functional
    tests:
        /tests/functional/pkgs/acl/test_acl_acl_inheritance
        /tests/functional/pkgs/acl/test_acl_acl_permission_verify
        ...
total: 11 tests
```

执行过程大约需要 **20~30 分钟**（取决于服务器性能）。每个测试用例的输出会实时显示在终端中。

### 9.6 查看结果

#### 方式一：查看汇总报告

```bash
cd ~/openruyi-autotest
tmt run --last report
```

输出示例：

```
total: 11 tests passed
```

#### 方式二：遍历所有 output.txt

```bash
RUN_DIR=$(ls -dt /var/tmp/tmt/run-* | head -1)
BASE="$RUN_DIR/plans/functional/execute/data/guest/default-0"

find "$BASE" -name "output.txt" | sort | while read f; do
    echo "=== $(basename $(dirname "$f")) ==="
    tail -3 "$f"
    echo ""
done
```

预期每个用例最后一行都是 `EXIT_CODE=0` 和 `TESTS_RESULT=PASS`。

#### 方式三：查看单个用例的输出

```bash
BASE="/var/tmp/tmt/run-*/plans/functional/execute/data/guest/default-0"
cat "$BASE/tests/functional/pkgs/acl/test_acl_getfacl_basic-1/output.txt"
```

### 9.7 ACL 测试套包含的用例

| 序号 | 用例名 | 说明 |
|------|--------|------|
| 1 | `test_acl_acl_inheritance` | ACL 权限继承验证 |
| 2 | `test_acl_acl_permission_verify` | ACL 权限正确性验证 |
| 3 | `test_acl_chacl_command` | chacl 命令功能测试 |
| 4 | `test_acl_error_handling` | 错误处理与边界情况 |
| 5 | `test_acl_getfacl_basic` | getfacl 基本功能 |
| 6 | `test_acl_getfacl_command` | getfacl 命令行选项 |
| 7 | `test_acl_setfacl_basic` | setfacl 基本功能 |
| 8 | `test_acl_setfacl_default_acl` | setfacl 默认 ACL |
| 9 | `test_acl_setfacl_modify_acl` | setfacl 修改已有 ACL |
| 10 | `test_acl_setfacl_recursive` | setfacl 递归操作 |
| 11 | `test_acl_tool_installation` | ACL 工具安装检查 |

> 共 11 个用例，全部通过即为 ACL 功能正常。此套件可作为其他软件包测试的参考模板。其他 `tests/functional/pkgs/<包名>/` 下的测试套执行方式与此完全相同，只需将 `test --name` 中的 `acl` 替换为目标包名即可。

---

## 10. 实战示例：K8s 特性测试（RISC-V）

本节以 `feature/k8s` 测试套为例，展示如何在 RISC-V 架构的 K8s 集群上执行特性测试。

### 10.1 前提条件

- **2 台 RISC-V 服务器**（1 个 K8s master + 1 个 worker 节点）
- 服务器已安装 K8s 集群（v1.35+），Calico CNI，containerd 运行时
- 每台服务器最低配置：**8 核 CPU，8 GiB 内存，1 个网卡**
- 每台服务器已安装 `beakerlib`、`sshpass`（参考第 1 节）

> **K8s 环境说明**：RISC-V 服务器上 `/etc/kubernetes/admin.conf` 通常属于 root 用户（权限 600），测试脚本会自动通过 `sudo` 调用 `kubectl`。

### 10.2 克隆仓库并安装依赖

在 master 节点上执行：

```bash
git clone https://git.openruyi.cn/woqidaideshi/openruyi-autotest.git
cd openruyi-autotest

# 安装 beakerlib 和 sshpass
sudo dnf install -y beakerlib sshpass

# riscv64 架构如需安装 tmt（可选，直接 bash 执行不需要 tmt）
sudo pip3 install --break-system-packages tmt
```

### 10.3 配置 topology.env

K8s 测试需要 2 台服务器，**必须配置 `topology.env`**：

```bash
cp topology.env.example topology.env
vim topology.env
```

写入内容（示例为 10.20.238.253 上的 2 节点 K8s 集群）：

```ini
TEST_SERVER_COUNT=2

# Server 1: K8s master 节点
TEST_SERVER_1_HOST=10.20.238.253
TEST_SERVER_1_PORT=12055
TEST_SERVER_1_USER=openruyi
TEST_SERVER_1_PASSWORD=openruyi

# Server 2: K8s worker 节点
TEST_SERVER_2_HOST=10.20.238.253
TEST_SERVER_2_PORT=12056
TEST_SERVER_2_USER=openruyi
TEST_SERVER_2_PASSWORD=openruyi
```

### 10.4 执行 K8s 快速健康检查

K8s 测试套提供了 **6 个子分类**，建议先执行 `quick` 快速验证集群是否正常：

```bash
cd ~/openruyi-autotest

# 方式一：使用 tmt 执行（单个用例）
tmt run --all --verbose plan --name /plans/feature \
    test --name /tests/feature/k8s/test_k8s_quick_health_check \
    provision --feeling-safe

# 方式二：直接 bash 执行（推荐，更快速）
TMT_TEST_TOPOLOGY_FILE="$PWD/topology.env" \
    bash tests/feature/k8s/test_k8s_quick_health_check.sh
```

**预期输出：**

```
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::   Verify kubectl is available
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: [ ... ] :: [   PASS   ] :: kubectl client is installed

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::   Verify K8s cluster nodes status
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: [ ... ] :: [   PASS   ] :: List cluster nodes
:: [ ... ] :: [   PASS   ] :: All nodes are in Ready state
:: [ ... ] :: [   PASS   ] :: Cluster has 2 nodes (>= 2)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::   Verify kube-system pods are running
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: [ ... ] :: [   PASS   ] :: At least N kube-system pods are Running

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::   Verify CoreDNS is running
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: [ ... ] :: [   PASS   ] :: CoreDNS has N Running pod(s)
```

### 10.5 执行全部 K8s 测试

```bash
cd ~/openruyi-autotest

# 使用 tmt 一次性执行所有 k8s 测试
tmt run --all --verbose plan --name /plans/feature \
    test --name /tests/feature/k8s \
    provision --feeling-safe
```

> **注意**：完整执行大约需要 **30 分钟**，具体时间取决于集群性能。

### 10.6 K8s 测试分类说明

| 分类 | 测试脚本 | 说明 | 预计耗时 |
|------|----------|------|----------|
| `quick` | `test_k8s_quick_health_check.sh` | 快速冒烟测试，验证集群基本健康 | ~5 分钟 |
| `conformance` | `test_k8s_conformance_pod_lifecycle.sh` | Pod 生命周期管理（创建、删除、扩缩容） | ~8 分钟 |
| `network` | `test_k8s_network_cross_node_communication.sh` | 跨节点网络通信（ClusterIP、NodePort、DNS） | ~5 分钟 |
| `storage` | `test_k8s_storage_pvc_lifecycle.sh` | PVC 存储卷生命周期（挂载、写入、持久化） | ~5 分钟 |
| `scheduling` | `test_k8s_scheduling_pod_affinity.sh` | Pod 调度策略（亲和性、nodeSelector、配额） | ~5 分钟 |
| `workload` | `test_k8s_workload_config_primitives.sh` | 工作负载配置（ConfigMap、Secret、ServiceAccount） | ~5 分钟 |
| `kata` | `test_k8s_kata_containers_runtime.sh` | Kata 安全容器运行时验证 | ~10 分钟 |

每个测试脚本都可单独执行：

```bash
# 例如只执行网络测试
TMT_TEST_TOPOLOGY_FILE="$PWD/topology.env" \
    bash tests/feature/k8s/test_k8s_network_cross_node_communication.sh

# 只执行存储测试
TMT_TEST_TOPOLOGY_FILE="$PWD/topology.env" \
    bash tests/feature/k8s/test_k8s_storage_pvc_lifecycle.sh
```

### 10.7 查看测试结果

使用 `tmt run` 执行时，结果存放在 `/var/tmp/tmt/run-*` 目录下（参考第 5 节）。

直接 bash 执行时，beakerlib 会在终端实时输出结果，最终显示汇总：

```
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::   OVERALL RESULT: PASS (unknown)
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
```

各阶段的详细日志临时存放在 `/var/tmp/beakerlib-*` 目录下。

### 10.8 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TMT_TEST_TOPOLOGY_FILE` | 拓扑配置文件路径 | 未设置时本地执行 |
| `K8S_KUBECONFIG` | kubectl 配置文件路径 | `/etc/kubernetes/admin.conf` |
| `K8S_USE_SUDO` | 是否使用 sudo 执行 kubectl | `true` |
