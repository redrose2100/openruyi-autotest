# 需求文档: K8s RISC-V 适配 Sonobuoy 等价测试用例开发

> **状态**: Confirmed ✅ | **创建时间**: 2026-07-23 | **作者**: AI (honghua)
> **自测报告**: [self-test-report.md](./self-test-report.md) — 25/25 100% 通过（2026-07-24）

---

## 评审确认记录

| 日期 | 评审人 | 确认项 | 结论 |
|------|--------|--------|------|
| 2026-07-23 | 用户 | 1. 优先级划分 | ✅ 认可 |
| 2026-07-23 | 用户 | 2. 24 个用例粒度 | ✅ 可以 |
| 2026-07-23 | 用户 | 3. Kata 容器支持 | ⚠️ 不确定，需实际验证；不支持则 SKIP |
| 2026-07-23 | 用户 | 4. Sonobuoy Smoke 范围 | ✅ 按飞书文档 SOP（自定义 RISC-V smoke 插件） |
| 2026-07-23 | 用户 | 5. 已有脚本处理 | ✅ 全部重构 |

---

## 1. 概述

### 1.1 需求来源

研发团队将 K8s 从 x86 架构适配到 RISC-V 架构，需要进行验证测试。

### 1.2 需求背景

- 研发已完成 K8s 的 RISC-V 架构适配（版本 v1.35.5）
- 需要通过**官方 Sonobuoy 工具**进行充分测试做为背书，证明适配没有问题
- **不能用自定义的用例验证**，需要以 Sonobuoy 覆盖的测试用例为基准
- 当前 `tests/feature/k8s/` 目录下有 8 个草稿级别的测试用例，需要**全部重构**
- 研发明确要求：**至少要用 Sonobuoy smoke 测试一下**
- **参考文档**: [openRuyi RISC-V QEMU 多节点 Kubernetes Nexus SOP](https://openruyi.feishu.cn/wiki/SWvdwvwOfizoQOkNZX5c4KRqn9b)（王玉锋，7月13日修改）

### 1.3 需求目标

基于 Sonobuoy 工具的测试覆盖范围，拆分为多个基于 tmt 框架的测试用例，每个用例遵循功能单一职责原则，不直接运行 Sonobuoy，而是将 Sonobuoy 覆盖的测试点映射为 tmt 脚本。

---

## 2. Sonobuoy 分析

### 2.1 Sonobuoy 简介

Sonobuoy 是 VMware Tanzu 维护的 Kubernetes 诊断工具，通过运行插件（主要是 Kubernetes e2e 测试）来验证集群状态。它是 CNCF 认证 Kubernetes 合规性的推荐工具。

### 2.2 Sonobuoy 内置模式

| 模式 | 说明 | 测试量 | 用途 |
|------|------|--------|------|
| `quick` | 运行 1 个简单快速的测试 | 1 个 | 快速检查集群可达性 |
| `non-disruptive-conformance` | 默认模式，运行非破坏性 Conformance 测试 | ~350+ | 在线集群合规检查 |
| `certified-conformance` | 运行所有 Conformance 测试（含破坏性） | ~380+ | CNCF 认证提交 |

### 2.3 Sonobuoy 测试覆盖的 SIG 领域

Sonobuoy 运行的是 Kubernetes 上游 e2e 测试，按 SIG 分组覆盖：

| SIG | 测试领域 | Conformance 测试数（估算） | 关键验证点 |
|-----|----------|--------------------------|-----------|
| **sig-api-machinery** | API 服务器、资源 CRUD、Watch、字段验证 | ~50+ | Pod/Deployment/Service 等资源的 CRUD、状态转换 |
| **sig-apps** | 工作负载管理 | ~30+ | Deployment 扩缩容、ReplicaSet、StatefulSet |
| **sig-network** | 网络通信 | ~40+ | Service（ClusterIP/NodePort）、DNS、Pod 间通信 |
| **sig-storage** | 存储卷 | ~30+ | PVC/PV 生命周期、Volume 挂载、数据持久化 |
| **sig-node** | 节点管理 | ~20+ | Pod 生命周期、容器运行时、资源限制 |
| **sig-scheduling** | 调度 | ~15+ | Pod 亲和性/反亲和性、nodeSelector、资源配额 |
| **sig-auth** | 认证授权 | ~15+ | ServiceAccount、RBAC、Secret |
| **sig-instrumentation** | 监控指标 | ~5+ | Metrics 端点 |
| **sig-cli** | kubectl 命令行 | ~10+ | kubectl apply/get/delete 等 |

> 注：具体数量随 Kubernetes 版本变化，v1.35 约 380+ Conformance 测试。非 Conformance 的 e2e 测试还包括性能、伸缩、特定提供商等。

### 2.4 Sonobuoy Smoke 测试分析

#### 2.4.1 飞书 SOP 文档中的 Sonobuoy Smoke

根据[飞书 SOP 文档](https://openruyi.feishu.cn/wiki/SWvdwvwOfizoQOkNZX5c4KRqn9b)第 11 节 "Sonobuoy smoke 验证"：

> **"本 SOP 中的 Sonobuoy 物料是 RISC-V smoke 验证，不是官方 conformance 测试。"**

**环境物料**:
- Sonobuoy 版本: **v0.57.3-riscv64**（RISC-V 定制版本）
- CLI 路径: `/opt/openruyi-k8s-multinode-assets/sonobuoy/bin/sonobuoy-v0.57.3-riscv64`
- 安装方式: `install -m 0755 <上述路径> /usr/local/bin/sonobuoy`
- Sonobuoy 镜像: `localhost/sonobuoy/sonobuoy:v0.57.3-riscv64`（已预导入到 containerd）
- 自定义插件: `/opt/openruyi-k8s-multinode-assets/manifests/openruyi-riscv-sonobuoy-smoke.yaml`

**运行命令**:
```bash
sonobuoy delete --kubeconfig /etc/kubernetes/admin.conf --wait || true

sonobuoy run \
  --kubeconfig /etc/kubernetes/admin.conf \
  --sonobuoy-image localhost/sonobuoy/sonobuoy:v0.57.3-riscv64 \
  --image-pull-policy Never \
  --force-image-pull-policy \
  --security-context-mode none \
  --plugin /opt/openruyi-k8s-multinode-assets/manifests/openruyi-riscv-sonobuoy-smoke.yaml \
  --skip-preflight=true \
  --timeout=900 \
  --wait=15
```

#### 2.4.2 自定义 Smoke 插件分析

SOP 使用的是**自定义 RISC-V smoke 插件**（非 Sonobuoy 官方的 `--mode quick`），该插件对应我们现有的 `test_k8s_sonobuoy_smoke.sh` 脚本，验证：
- 节点架构为 riscv64
- DNS 解析 `kubernetes.default.svc.cluster.local`
- 通过 ServiceAccount Token 访问 API Server `/version` 端点
- 以 DaemonSet 形式在每个节点上运行

#### 2.4.3 我们的策略

**不直接运行 `sonobuoy run`**，而是将 Sonobuoy smoke 插件的验证逻辑转换为 tmt + beakerlib 脚本，实现等价验证。同时保留运行真实 Sonobuoy smoke 的能力作为可选项。

---

## 3. 需求范围

### 3.1 范围之内 (In Scope)

1. **分析 Sonobuoy 覆盖的测试用例**，理解其覆盖的功能领域（已完成，见上表）
2. **基于 Sonobuoy 覆盖范围拆分为 tmt 测试用例**，每个用例遵循功能单一职责
3. **重点实现 Sonobuoy Smoke 级别测试用例**（研发明确要求）
4. **按优先级实现各领域测试用例**:
   - P0: Smoke / 集群健康检查
   - P1: Pod 生命周期、网络通信、存储
   - P2: 调度、ConfigMap/Secret、Kata 容器
5. **测试用例结构要求**:
   - 每个测试用例独立 "test_k8s_xxx" 名称
   - 在 `tests/feature/k8s/` 下用 tmt 框架 + beakerlib 编写
   - 使用 `lib.sh` 共享连接逻辑
   - 基于 `topology.env` 配置远程环境
6. **环境适配**:
   - 测试环境: CloudPods VM (10.20.238.229)，内含 2 个 RISC-V QEMU VM
   - Master: SSH 端口 12055，用户名/密码 `openruyi`/`openruyi`
   - Worker: SSH 端口 12056，用户名/密码 `openruyi`/`openruyi`
   - Sudo 密码: `openruyi`
7. **到 12055 端口的服务器上 git clone 并调试执行，如果脚本有问题则修改脚本，如果环境有问题则修改 `create_k8s_env.py`**

### 3.2 范围之外 (Out of Scope)

- 不直接运行 Sonobuoy 二进制（用等价 tmt 脚本替代）
- **但保留运行真实 Sonobuoy smoke 的能力**作为可选验证方式（验证等价脚本与真实 Sonobuoy 输出一致）
- 不提交 CNCF 认证（仅内部验证 RISC-V 适配）
- 不涉及 K8s 集群的创建（环境已由 `create_k8s_env.py` 创建好）
- 不涉及非 RISC-V 架构的测试
- 不使用 Sonobuoy 官方 Conformance 模式（SOP 中明确说明是 RISC-V smoke，非官方 conformance）

---

## 4. 功能描述

### 4.1 测试用例规划（基于 Sonobuoy 覆盖拆解）

#### 第一组: 集群健康检查 (对应 Sonobuoy Smoke)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_smoke_arch_check` | 自定义 RISC-V smoke 插件 | 所有节点架构为 riscv64（`kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'`） | 2m |
| `test_k8s_smoke_dns_resolve` | 自定义 RISC-V smoke 插件 | 从 Pod 内通过 nslookup 解析 `kubernetes.default.svc.cluster.local`，验证 CoreDNS 正常工作 | 3m |
| `test_k8s_smoke_api_reachable` | 自定义 RISC-V smoke 插件 | 从 Pod 内通过 ServiceAccount Token 访问 API Server `/version` 端点，验证返回 JSON 包含 `"major"` 字段 | 3m |
| `test_k8s_smoke_daemonset` | 自定义 RISC-V smoke 插件（复合测试） | 等效于飞书 SOP 中 `sonobuoy run --plugin openruyi-riscv-sonobuoy-smoke.yaml` 的 DaemonSet 方式：每节点运行一个 Pod，在 Pod 内依次验证架构、DNS、API Server 可达性 | 5m |

> **对照**: 飞书 SOP 中的 Sonobuoy smoke 通过自定义插件 `openruyi-riscv-sonobuoy-smoke.yaml` 实现，以 DaemonSet 方式在每个节点运行验证 Pod。我们将此拆为 4 个 tmt 用例：3 个原子验证 + 1 个集成验证。

#### 第二组: API 与资源管理 (对应 sig-api-machinery)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_api_resource_crud` | CRUD 操作 Conformance 测试 | Pod/Deployment/Service/ConfigMap 的 create/get/update/delete，字段验证，状态转换 | 10m |
| `test_k8s_api_namespace_lifecycle` | Namespace 相关测试 | Namespace 创建/删除、资源隔离、Terminating 状态处理 | 5m |

#### 第三组: Pod 生命周期 (对应 sig-node)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_pod_basic_lifecycle` | Pod 生命周期 Conformance | Pod 创建→Pending→Running→Succeeded/Failed，重启策略，探针 | 8m |
| `test_k8s_pod_multi_container` | 多容器 Pod 测试 | Init Container、Sidecar、共享卷、端口冲突 | 8m |

#### 第四组: 工作负载管理 (对应 sig-apps)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_workload_deployment` | Deployment Conformance 测试 | Deployment 创建/扩缩容/滚动更新/回滚 | 10m |
| `test_k8s_workload_replicaset` | ReplicaSet 测试 | ReplicaSet 创建、副本数维护、OwnerReference | 5m |

#### 第五组: 网络通信 (对应 sig-network)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_network_service_clusterip` | Service ClusterIP Conformance | ClusterIP 创建、Endpoints 更新、Pod-to-Service 通信 | 8m |
| `test_k8s_network_service_nodeport` | Service NodePort 测试 | NodePort 暴露、外部可达性、端口范围 | 5m |
| `test_k8s_network_dns` | DNS Conformance 测试 | CoreDNS 解析（Service FQDN、Pod FQDN、外部域名） | 5m |
| `test_k8s_network_cross_node_pod` | Pod-to-Pod 跨节点通信 | 不同节点上 Pod 通过 IP 和 Service 互相通信 | 8m |

#### 第六组: 存储 (对应 sig-storage)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_storage_pvc_binding` | PVC/PV Binding Conformance | PVC 创建→Pending→Bound、StorageClass 默认值 | 8m |
| `test_k8s_storage_volume_mount` | Volume Mount 测试 | EmptyDir/HostPath/PVC 挂载、读写验证 | 8m |
| `test_k8s_storage_data_persistence` | 数据持久化测试 | Pod 删除重建后 PVC 数据保留 | 5m |

#### 第七组: 调度 (对应 sig-scheduling)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_scheduling_nodeselector` | NodeSelector Conformance | nodeSelector 约束、调度成功/失败 | 5m |
| `test_k8s_scheduling_affinity` | Pod Affinity 测试 | required/preferred 亲和性与反亲和性 | 8m |
| `test_k8s_scheduling_taints_tolerations` | Taint/Toleration 测试 | NoSchedule/NoExecute toleration | 5m |
| `test_k8s_scheduling_resource_quota` | ResourceQuota 测试 | CPU/内存配额限制、超出限制拒绝 | 5m |

#### 第八组: 认证与配置 (对应 sig-auth)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_auth_serviceaccount` | ServiceAccount Conformance | SA 自动创建、Token 挂载、API Server 认证 | 5m |
| `test_k8s_config_secret` | Secret Conformance 测试 | Secret 创建/读取、环境变量注入、卷挂载 | 8m |
| `test_k8s_config_configmap` | ConfigMap Conformance 测试 | ConfigMap 创建/更新、环境变量/卷挂载、热更新 | 8m |

#### 第九组: Kata 容器 (RISC-V 特性)

| 用例名称 | 对应 Sonobuoy 覆盖 | 验证点 | 预估耗时 |
|----------|-------------------|--------|----------|
| `test_k8s_kata_runtime_basic` | 非 Sonobuoy (RISC-V 特性) | kata-clh RuntimeClass 验证、Pod 启动、内核隔离 | 10m |

### 4.2 环境拓扑

```
CloudPods 宿主机 (10.20.238.229)
├── RISC-V QEMU VM #1 (K8s Master)
│   ├── IP: 192.168.77.11
│   ├── SSH: 宿主机:12055 → VM:22
│   └── 用户: openruyi / openruyi (sudo: openruyi)
└── RISC-V QEMU VM #2 (K8s Worker)
    ├── IP: 192.168.77.12
    ├── SSH: 宿主机:12056 → VM:22
    └── 用户: openruyi / openruyi (sudo: openruyi)
```

### 4.3 验收标准

- [x] 所有用例通过 tmt 框架可以正常执行
- [x] 每个用例覆盖的功能点与 Sonobuoy Conformance 测试对齐
- [x] Sonobuoy Smoke 级别用例全部通过（研发明确要求）
- [x] 测试脚本在 12055/12056 环境上经过实际调试并 PASS
- [x] 如发现脚本问题，脚本已修复（4 个脚本修复，详见自测报告）
- [x] 如发现环境问题，CoreDNS loop 已修复
- [x] 现有 `tests/feature/k8s/` 下的 8 个草稿脚本已重构合并到新用例

> 详细自测结果见 [self-test-report.md](./self-test-report.md)

---

## 5. 非功能性需求

### 5.1 性能要求

- 单个用例运行时间 ≤ 15 分钟
- 全量用例运行时间建议 ≤ 2 小时

### 5.2 安全要求

- 不在脚本中硬编码密码（使用 topology.env 变量）
- SSH 使用 sshpass 或密钥认证

### 5.3 可维护性要求

- 每个测试用例文件单一职责，不超过 200 行
- 公共逻辑提取到 `lib.sh`
- FMF metadata 标注对应的 Sonobuoy SIG 和测试类别
- 命名规范统一: `test_k8s_<领域>_<具体功能>.sh`

---

## 6. 约束与假设

### 6.1 约束条件

- K8s 集群已由 `create_k8s_env.py` 在 CloudPods 上创建完成
- 测试环境无法直接访问外网（镜像已预导入）
- 使用 tmt + beakerlib 测试框架（`rlRun`、`rlAssert`、`rlPhase`）
- Gitea 提交仅限 ASCII 英文（commit message 和 MR 标题）

### 6.2 假设条件

- 集群中 Calico CNI、CoreDNS、local-path-provisioner 已正确部署
- 所有必需的容器镜像已通过 Nexus 导入到 containerd
- RISC-V 架构下 Kata Containers (`kata-clh`) 已安装

---

## 7. 风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| RISC-V 环境下某些容器镜像不可用 | 阻塞网络/存储/Pod 测试 | 中 | 提前验证镜像可用性，准备替代镜像 |
| K8s v1.35.5 在 RISC-V 上存在未发现的 Bug | 测试 FAIL | 高 | 区分环境 Bug vs 脚本 Bug，及时反馈研发 |
| Sonobuoy 某些 Conformance 测试在 RISC-V 上不适用（如 LinuxOnly） | 部分用例无法等价 | 低 | 标记为 SKIP 并说明原因 |
| QEMU 模拟性能不稳定导致超时 | 测试 FLAKY | 中 | 适当放宽超时设置 |

---

## 8. 附录

### 8.1 参考资料

- **飞书 SOP 文档**: [openRuyi RISC-V QEMU 多节点 Kubernetes Nexus SOP](https://openruyi.feishu.cn/wiki/SWvdwvwOfizoQOkNZX5c4KRqn9b)（王玉锋，7月13日修改）— 第 11 节 Sonobuoy smoke 验证
- Sonobuoy 官方文档: https://sonobuoy.io/docs/main/
- Sonobuoy GitHub: https://github.com/vmware-tanzu/sonobuoy
- K8s Conformance 测试定义: https://github.com/kubernetes/kubernetes/blob/master/test/conformance/testdata/conformance.yaml
- K8s Conformance 规范: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/conformance-tests.md
- CNCF K8s Conformance: https://github.com/cncf/k8s-conformance

### 8.2 术语表

| 术语 | 说明 |
|------|------|
| Sonobuoy | VMware 维护的 K8s 合规性诊断工具 |
| Conformance | K8s 合规性测试子集（~380+ 测试） |
| tmt | Test Management Tool，Fedora 的测试管理框架 |
| FMF | Flexible Metadata Format，tmt 的元数据格式 |
| beakerlib | Shell 测试库，提供 rlRun/rlAssert 等函数 |
| SIG | Special Interest Group，K8s 社区按领域分的特别兴趣小组 |
| CloudPods | 云管理平台，用于创建 KVM 虚拟机 |
| kata-clh | Kata Containers 的 Cloud Hypervisor runtime |
