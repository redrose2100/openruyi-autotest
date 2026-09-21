# Test Reports

> Test execution time: YYYY-MM-DD HH:MM
> Test environment: openRuyi Creek, kernel xxx, riscv64

---

## Overview

### Summary

This test run covers seven categories — Smoke, Functional, Security, Performance, Compatibility, Reliability, and Feature tests — executed via the tmt framework with BeakerLib scripts.

### Test Environment

| Item | Description |
|------|-------------|
| **System Under Test** | openRuyi Creek |
| **Kernel Version** | xxx |
| **Architecture** | riscv64 |
| **Test Framework** | tmt x.x.x |
| **Test Tool** | BeakerLib |
| **Execution Mode** | `tmt run --all provision --how local --feeling-safe` |

### Overall Results

| Test Type | Suites | Cases | Pass | Fail | Skip | Pass Rate |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| Smoke | 100 | 100 | - | - | - | - |
| Functional | 202 | 1103 | - | - | - | - |
| Security | 106 | 106 | - | - | - | - |
| Performance | 7 | 7 | - | - | - | - |
| Compatibility | 188 | 188 | - | - | - | - |
| Reliability | 1 | 1 | - | - | - | - |
| Feature | 0 | 0 | - | - | - | - |
M0505** | - | - | - | - |

---

## Smoke Tests

| Test Suite | Cases | Pass | Fail | Skip | Status |
|------------|:---:|:---:|:---:|:---:|:---:|
| archive | 5 | - | - | - | - |
| dev_tools | 6 | - | - | - | - |
| disk_fs | 6 | - | - | - | - |
| filesystem | 6 | - | - | - | - |
| kernel | 6 | - | - | - | - |
| logging | 6 | - | - | - | - |
| network | 8 | - | - | - | - |
| package_mgmt | 5 | - | - | - | - |
| permissions | 6 | - | - | - | - |
| process | 6 | - | - | - | - |
| scripting | 7 | - | - | - | - |
| security | 6 | - | - | - | - |
| service_mgmt | 6 | - | - | - | - |
| shell_basics | 8 | - | - | - | - |
| system_info | 6 | - | - | - | - |
| text_processing | 7 | - | - | - | - |
| user_mgmt | 6 | - | - | - | - |
| **Total** | **100** | - | - | - | - |

---

## Functional Tests

| Category | Packages | Cases | Pass | Fail | Skip | Status |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|
| pkgs | 202 | 566 | - | - | - | - |
M0505** | - | - | - | - |

---

## Security Tests

| Test Suite | Cases | Pass | Fail | Skip | Status |
|------------|:---:|:---:|:---:|:---:|:---:|
| CVE | - | - | - | - | - |
| Nmap | - | - | - | - | - |
| **Total** | **106** | - | - | - | - |

---

## Performance Tests

| Test Suite | Cases | Pass | Fail | Skip | Status |
|------------|:---:|:---:|:---:|:---:|:---:|
| UnixBench | 7 | - | - | - | - |
| **Total** | **7** | - | - | - | - |

---

## Compatibility Tests

| Test Suite | Cases | Pass | Fail | Skip | Status |
|------------|:---:|:---:|:---:|:---:|:---:|
| LTP POSIX | 188 | - | - | - | - |
| **Total** | **188** | - | - | - | - |

---

## Reliability Tests

| Test Suite | Cases | Pass | Fail | Skip | Status |
|------------|:---:|:---:|:---:|:---:|:---:|
| Reliability | 1 | - | - | - | - |
| **Total** | **1** | - | - | - | - |

---

## Feature Tests

TBD.
