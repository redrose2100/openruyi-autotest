# 安全测试覆盖详情

> 最后更新: 2026-06-15 | 自动生成
> 测试环境: openRuyi RISC-V (10.20.237.192)

共 **2** 个安全测试套件，**106** 个测试用例，**124** 个功能点

## 安全测试套件一览

| 测试套件 | 用例数 | 功能点 | PASS | FAIL | SKIP | TIMEOUT | 类型 |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [nmap](#nmap) | 8 | 26 | 8 | 0 | 0 | 0 | rlRun |
| [cve](#cve) | 98 | 98 | 74 | 0 | 24 | 0 | LTP (runltp) |

---

## nmap

<details>
<summary><b>nmap — 8 个用例 / 26 个功能点</b></summary>

#### test_nmap_basic_scan

- TCP 端口扫描 (常用端口)
- UDP 端口扫描 (DNS)
- TCP 端口扫描 (1-100)

#### test_nmap_service_detection

- SSH 服务版本检测
- 服务版本探测

#### test_nmap_os_detection

- 操作系统指纹识别
- 限制型 OS 检测

#### test_nmap_script_scan

- NSE banner 脚本
- NSE HTTP 头检测
- NSE SSH 认证方法检测
- NSE SSL 密码套件枚举

#### test_nmap_firewall_evasion

- 分片包扫描 (fragment)
- 随机数据填充扫描
- 错误校验和探测

#### test_nmap_network_discovery

- Ping 扫描 (主机发现)
- ICMP Echo 发现
- TCP SYN Ping 发现

#### test_nmap_ssl_analysis

- SSL 证书分析
- Heartbleed 漏洞检测
- SSLv2 支持检测

#### test_nmap_output_formats

- 普通格式输出 (-oN)
- XML 格式输出 (-oX)
- Grepable 格式输出 (-oG)
- 全格式输出 (-oA)
- 普通输出文件存在
- XML 输出文件存在
- Grepable 输出文件存在

</details>

## 安全测试覆盖场景

| 场景类别 | 覆盖内容 | nmap 命令示例 |
|----------|---------|-------------|
| **端口扫描** | TCP/UDP 端口发现 | `nmap -T4 -p 1-100` / `nmap -sU -p 53` |
| **服务检测** | 服务版本识别 | `nmap -sV -p 22` |
| **OS 指纹** | 操作系统识别 | `nmap -O --osscan-limit` |
| **NSE 脚本** | 漏洞/信息探测 | `nmap --script=banner,ssl-enum-ciphers` |
| **规避技术** | 防火墙/IDS 绕过 | `nmap -f` / `nmap --data-length` / `nmap --badsum` |
| **主机发现** | 存活主机探测 | `nmap -sn` / `nmap -PE` / `nmap -PS` |
| **SSL/TLS** | 证书/密码分析 | `nmap --script=ssl-cert,ssl-heartbleed,sslv2` |
| **输出格式** | 多格式报告 | `nmap -oN/-oX/-oG/-oA` |

---

## cve

<details>
<summary><b>cve — 98 个用例 / 98 个功能点（74P / 24S / 0F）</b></summary>

> **数据来源**: [LTP (Linux Test Project)](https://github.com/linux-test-project/ltp) runtest/cve
> **测试方式**: `sudo ./runltp -f cve` 原生运行（93 个），另有 5 个新 CVE 直接运行 LTP 二进制
> **实事求是**: PASS=系统已修复该漏洞；SKIP=测试不适用或二进制不存在；FAIL=0 表示系统对所有已知 CVE 已修复

### PASS（系统已修复，74 个）

| CVE ID | CVE ID | CVE ID | CVE ID |
|--------|--------|--------|--------|
| cve-2011-0999 | cve-2011-2183 | cve-2012-0957 | cve-2014-0196 |
| cve-2015-0235 | cve-2015-7550 | cve-2016-4470 | cve-2016-4997 |
| cve-2016-5195 | cve-2016-7042 | cve-2016-7117 | cve-2016-8655 |
| cve-2016-9604 | cve-2016-9793 | cve-2016-10044 | cve-2017-2618 |
| cve-2017-2636 | cve-2017-2671 | cve-2017-6951 | cve-2017-7308 |
| cve-2017-7472 | cve-2017-8890 | cve-2017-10661 | cve-2017-12192 |
| cve-2017-12193 | cve-2017-15274 | cve-2017-15299 | cve-2017-15649 |
| cve-2017-15951 | cve-2017-16939 | cve-2017-16995 | cve-2017-17052 |
| cve-2017-17712 | cve-2017-17806 | cve-2017-17807 | cve-2017-18344 |
| cve-2017-1000111 | cve-2017-1000112 | cve-2017-1000364 | cve-2017-1000380 |
| cve-2017-1000405 | cve-2018-5803 | cve-2018-6927 | cve-2018-9568 |
| cve-2018-11508 | cve-2018-12896 | cve-2018-13405 | cve-2018-18445 |
| cve-2018-18559 | cve-2018-18955 | cve-2018-19854 | cve-2018-1000001 |
| cve-2019-8912 | cve-2020-11494 | cve-2020-14386 | cve-2020-14416 |
| cve-2020-25705 | cve-2020-29373 | cve-2020-36557 | cve-2021-3609 |
| cve-2021-4034 | cve-2021-4197_1 | cve-2021-4197_2 | cve-2021-26708 |
| cve-2021-22600 | cve-2021-38604 | cve-2022-0847 | cve-2022-2590 |
| cve-2022-0185 | cve-2022-4378 | cve-2023-0461 | cve-2023-31248 |
| cve-2025-21756 | cve-2025-38236 |

### SKIP（不适用或二进制不可用，24 个）

| CVE ID | 原因 |
|--------|------|
| cve-2011-2496 | RISC-V 不适用 |
| cve-2015-3290 | RISC-V 不适用 |
| cve-2017-5754 | RISC-V 不适用 (Meltdown) |
| cve-2017-7616 | RISC-V 不适用 |
| cve-2017-15537 | RISC-V 不适用 |
| cve-2017-17053 | RISC-V 不适用 |
| cve-2017-17805 | RISC-V 不适用 |
| cve-2017-18075 | RISC-V 不适用 |
| cve-2018-7566 | RISC-V 不适用 |
| cve-2018-8897 | RISC-V 不适用 |
| cve-2018-10124 | RISC-V 不适用 |
| cve-2018-1000199 | RISC-V 不适用 |
| cve-2018-1000204 | RISC-V 不适用 |
| cve-2020-25704 | RISC-V 不适用 |
| cve-2021-3444 | RISC-V 不适用 |
| cve-2021-4204 | RISC-V 不适用 |
| cve-2021-22555 | RISC-V 不适用 |
| cve-2022-23222 | RISC-V 不适用 |
| cve-2023-1829 | RISC-V 不适用 |
| cve-2026-31431 | LTP 二进制不可用 |
| cve-2026-43284 | LTP 二进制不可用 |
| cve-2026-43494 | LTP 二进制不可用 |
| cve-2026-46300 | LTP 二进制不可用 |
| cve-2026-46300-skb-segment | LTP 二进制不可用 |

### 新旧对比

| 指标 | 旧方案（直接二进制） | 新方案（runltp -f cve） |
|------|:---:|:---:|
| PASS | 38 | **74** (+36) |
| FAIL | 7 | **0** (-7) |
| SKIP | 47 | 19 (-28) |
| TIMEOUT | 6 | **0** (-6) |
| 通过率 | 38.8% | **75.5%** |

</details>

---

## 运行安全测试

```bash
# 单独运行 nmap 安全测试
cd tests/security/nmap && bash test.sh

# 运行 CVE 安全测试（需 LTP 环境）
cd tests/security/cve && bash run_all.sh

# 在服务器上运行
ssh openruyi@10.20.237.192 -p 12055
cd /path/to/tests/security/nmap && bash test.sh
```

## 安全说明

- 所有测试仅针对 localhost (127.0.0.1) 执行，不会扫描外部网络
- 部分功能（OS 指纹识别）需要 root 权限，非 root 环境下会自动跳过
- 扫描使用 `-T4` 和 `--host-timeout` 参数控制时间
- 如发现危险端口开放（telnet 23、FTP 21、RDP 3389 等），测试会发出警告
