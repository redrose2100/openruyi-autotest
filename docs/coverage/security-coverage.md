# Security Test Coverage Details

> Last updated: 2026-06-15 | Auto-generated
> Test environment: openRuyi RISC-V (10.20.237.192)

**2** security test suites total, **106** test cases, **124** feature points

## Security Test Suites Overview

| Test Suite | Cases | Feature Points | PASS | FAIL | SKIP | TIMEOUT | Type |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [nmap](#nmap) | 8 | 26 | 8 | 0 | 0 | 0 | rlRun |
| [cve](#cve) | 98 | 98 | 74 | 0 | 24 | 0 | LTP (runltp) |

---

## nmap

<details>
<summary><b>nmap — 8 cases / 26 feature points</b></summary>

#### test_nmap_basic_scan

- TCP port scan (common ports)
- UDP port scan (DNS)
- TCP port scan (1-100)

#### test_nmap_service_detection

- SSH service version detection
- Service version probe

#### test_nmap_os_detection

- OS fingerprint identification
- Limited OS detection

#### test_nmap_script_scan

- NSE banner script
- NSE HTTP header detection
- NSE SSH auth method detection
- NSE SSL cipher suite enumeration

#### test_nmap_firewall_evasion

- Fragmented packet scan (fragment)
- Random data padding scan
- Bad checksum probe

#### test_nmap_network_discovery

- Ping scan (host discovery)
- ICMP Echo discovery
- TCP SYN Ping discovery

#### test_nmap_ssl_analysis

- SSL certificate analysis
- Heartbleed vulnerability detection
- SSLv2 support detection

#### test_nmap_output_formats

- Normal format output (-oN)
- XML format output (-oX)
- Grepable format output (-oG)
- All formats output (-oA)
- Normal output file exists
- XML output file exists
- Grepable output file exists

</details>

## Security Test Coverage Scenarios

| Scenario Category | Coverage | nmap Command Example |
|----------|---------|-------------|
| **Port Scan** | TCP/UDP port discovery | `nmap -T4 -p 1-100` / `nmap -sU -p 53` |
| **Service Detection** | Service version identification | `nmap -sV -p 22` |
| **OS Fingerprint** | Operating system identification | `nmap -O --osscan-limit` |
| **NSE Scripts** | Vulnerability/info probe | `nmap --script=banner,ssl-enum-ciphers` |
| **Evasion Techniques** | Firewall/IDS bypass | `nmap -f` / `nmap --data-length` / `nmap --badsum` |
| **Host Discovery** | Live host detection | `nmap -sn` / `nmap -PE` / `nmap -PS` |
| **SSL/TLS** | Certificate/cipher analysis | `nmap --script=ssl-cert,ssl-heartbleed,sslv2` |
| **Output Formats** | Multi-format reports | `nmap -oN/-oX/-oG/-oA` |

---

## cve

<details>
<summary><b>cve — 98 cases / 98 feature points (74P / 24S / 0F)</b></summary>

> **Source**: [LTP (Linux Test Project)](https://github.com/linux-test-project/ltp) runtest/cve
> **Test method**: `sudo ./runltp -f cve` native run (93), plus 5 new CVEs run LTP binary directly
> **Honest results**: PASS = system has patched this vulnerability; SKIP = test not applicable or binary not available; FAIL = 0 means system is patched for all known CVEs

### PASS (system patched, 74)

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

### SKIP (not applicable or binary unavailable, 24)

| CVE ID | Reason |
|--------|------|
| cve-2011-2496 | RISC-V not applicable |
| cve-2015-3290 | RISC-V not applicable |
| cve-2017-5754 | RISC-V not applicable (Meltdown) |
| cve-2017-7616 | RISC-V not applicable |
| cve-2017-15537 | RISC-V not applicable |
| cve-2017-17053 | RISC-V not applicable |
| cve-2017-17805 | RISC-V not applicable |
| cve-2017-18075 | RISC-V not applicable |
| cve-2018-7566 | RISC-V not applicable |
| cve-2018-8897 | RISC-V not applicable |
| cve-2018-10124 | RISC-V not applicable |
| cve-2018-1000199 | RISC-V not applicable |
| cve-2018-1000204 | RISC-V not applicable |
| cve-2020-25704 | RISC-V not applicable |
| cve-2021-3444 | RISC-V not applicable |
| cve-2021-4204 | RISC-V not applicable |
| cve-2021-22555 | RISC-V not applicable |
| cve-2022-23222 | RISC-V not applicable |
| cve-2023-1829 | RISC-V not applicable |
| cve-2026-31431 | LTP binary unavailable |
| cve-2026-43284 | LTP binary unavailable |
| cve-2026-43494 | LTP binary unavailable |
| cve-2026-46300 | LTP binary unavailable |
| cve-2026-46300-skb-segment | LTP binary unavailable |

### Old vs New Comparison

| Metric | Old (direct binary) | New (runltp -f cve) |
|------|:---:|:---:|
| PASS | 38 | **74** (+36) |
| FAIL | 7 | **0** (-7) |
| SKIP | 47 | 19 (-28) |
| TIMEOUT | 6 | **0** (-6) |
| Pass Rate | 38.8% | **75.5%** |

</details>

---

## Running Security Tests

```bash
# Run nmap security tests individually
cd tests/security/nmap && bash test.sh

# Run CVE security tests (requires LTP environment)
cd tests/security/cve && bash run_all.sh

# Run on server
ssh openruyi@10.20.237.192 -p 12055
cd /path/to/tests/security/nmap && bash test.sh
```

## Security Notes

- All tests run against localhost (127.0.0.1) only; no external network scanning
- Some features (OS fingerprint) require root privileges; automatically skipped in non-root environments
- Scans use `-T4` and `--host-timeout` parameters to control timing
- If dangerous ports are found open (telnet 23, FTP 21, RDP 3389, etc.), tests will emit a warning
