# CloudPods 工具规范

> `tools/cloudpods/` 目录下的 CloudPods 集成工具规范。

---

## 概述

CloudPods 是 openEuler RISC-V 的测试资源管理平台，本项目的 `tools/cloudpods/` 提供创建 K8s 集群和虚拟服务器的 Python 工具。

---

## 目录结构

```
tools/cloudpods/
├── __init__.py
├── create_k8s_env.py       # 创建 K8s 集群环境
├── create_server.py        # 创建/管理虚拟机
└── requirements.txt        # 依赖（paramiko, requests 等）
```

---

## 设计原则

- **幂等性**：重复调用 `create_server.py` 不会创建重复资源
- **显式清理**：提供明确的清理/释放接口
- **凭证外置**：通过环境变量或配置文件读取 API 密钥

---

## 使用方式

```bash
# 安装依赖
pip install -r tools/cloudpods/requirements.txt

# 创建测试服务器
python tools/cloudpods/create_server.py --name test-vm --cpu 4 --memory 8G

# 创建 K8s 集群
python tools/cloudpods/create_k8s_env.py --name test-cluster --nodes 3
```

---

## 凭证管理

- CloudPods API 凭证通过环境变量读取（如 `CLOUDPODS_ACCESS_KEY`）
- **绝不**硬编码在代码中
- 在 CI 中通过 GitHub Secrets 注入

---

## 错误处理

```python
# ✅ 正确：明确异常类型 + 有意义的消息
try:
    server = client.create_server(name="test-vm")
except CloudPodsAPIError as e:
    logger.error("创建服务器失败: %s", e)
    raise SystemExit(1)

# ❌ 错误：裸 except
try:
    server = client.create_server(name="test-vm")
except:
    pass
```

---

## 添加新工具

1. 在 `tools/cloudpods/` 下新建 `.py` 文件
2. 如引入新依赖，更新 `requirements.txt`
3. 在文件头部用 `"""..."""` 说明用途和用法