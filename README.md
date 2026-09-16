# openruyi-autotest

openruyi-autotest is an automated testing project based on the [tmt (Test Management Tool)](https://tmt.readthedocs.io/) framework, using [BeakerLib](https://github.com/beakerlib/beakerlib) for test scripts and [FMF](https://fmf.readthedocs.io/) for metadata management. It covers seven categories: Smoke, Functional, Security, Compatibility, Performance, Reliability, and Feature tests, totaling 726 test suites and 3,708 test cases (Functional: 281 suites / 3,216 cases — 566 pkgs + 2,407 LTP + 211 kernel + 32 compiler; Security: 113 suites / 113 cases — 98 CVE + 8 nmap + 7 openscap; Reliability: 12 suites / 12 cases — 6 trinity + 6 stress-ng).

> :cn: [中文版 (Chinese Version)](README_CN.md)

---

## 1. Introduction

### 1.1 Directory Structure

```
openruyi-autotest/
├── .fmf/                        # FMF metadata root
│   └── version
├── plans/                       # Test plans
│   ├── smoke.fmf                 # Smoke test plan
│   ├── functional.fmf            # Functional test plan
│   ├── security.fmf              # Security test plan
│   ├── compatibility.fmf         # Compatibility test plan
│   ├── performance.fmf           # Performance test plan
│   ├── reliability.fmf           # Reliability test plan
│   ├── feature.fmf               # Feature test plan
│   └── all.fmf                   # Full test plan
├── tests/                       # Test cases
│   ├── main.fmf                  # Global shared configuration
│   ├── smoke/                    # Smoke tests (100 cases)
│   ├── functional/               # Functional tests
│   │   ├── kernel/               # Kernel functional tests
│   │   │   ├── blktests/         #   Block device tests (195 cases)
│   │   │   └── realtime/         #   Real-time tests (16 cases)
│   │   ├── ltp/                  # LTP functional test suite (32 sub-modules, 2,407 cases)
│   │   ├── pkgs/                 # RPM package functional tests (202 packages, 566 cases)
│   │   └── compiler/             # Compiler & toolchain tests (32 cases)
│   │       ├── dejagnu/          #   DejaGnu GCC test framework (9 cases)
│   │       ├── jotai/            #   Jotai benchmark tests (7 cases)
│   │       ├── csmith/           #   Csmith random program differential testing (8 cases)
│   │       └── yarpgen/          #   YARPGen optimization bug detection (8 cases)
│   ├── security/                 # Security tests (113 cases)
│   │   ├── cve/                  # CVE vulnerability tests (98 cases)
│   │   ├── nmap/                 # Network scanning tests (8 cases)
│   │   ├── openscap/             # Security compliance tests (7 cases: 4 basic + 3 CIS)
│   │   │   ├── basic/             #   Basic CLI operations (4 cases)
│   │   │   └── cis/               #   CIS Benchmark (3 cases)
│   ├── compatibility/            # Compatibility tests (188 cases)
│   ├── performance/              # Performance tests
│   │   ├── mmtests/              #   MMTests benchmarks (53 cases)
│   │   ├── unixbench/            #   UnixBench benchmarks (11 cases)
│   │   ├── iozone/               #   IOzone filesystem I/O benchmarks (5 cases)
│   │   ├── fio/                  #   fio storage I/O performance tests (6 cases)
│   │   ├── stream/               #   STREAM memory bandwidth benchmarks (4 cases)
│   │   ├── lmbench/              #   LMbench micro-benchmarks (4 cases)
│   │   └── sysbench/             #   sysbench multi-threaded benchmarks (5 cases)
│   ├── feature/                  # Feature tests
│   └── reliability/              # Reliability tests
│       ├── trinity/              #   Trinity syscall fuzzer (6 cases)
│       └── stress-ng/            #   stress-ng system stress tests (6 cases)
├── docs/                        # Documentation
└── README.md
```

### 1.2 Test Coverage Details

| Category | Representative Packages | Coverage Highlights |
|----------|------------------------|---------------------|
| **Build Tools** | gcc, g++ (gxx), clang, cmake, make, binutils, autoconf, automake, bison, flex, meson, ninja | C/C++ compilation, linking, optimization options, standard support |
| **System Management** | systemd, systemd-timesyncd, dbus, dbus-broker, chkconfig, kmod, util-linux | Service management, log query, performance analysis, time sync |
| **File/Text Tools** | coreutils, tar, grep, sed, gawk, diffutils, findutils, file, gzip, xz, zstd, bzip2, lz4, unzip, cpio, dos2unix | File operations, archiving, search, text processing |
| **Security/Crypto** | openssl, gnutls, libgcrypt, nettle, libtasn1, p11-kit, cryptsetup, pam, libselinux, libseccomp, audit, keyutils, krb5 | Encryption algorithms, TLS, ACL, auditing, authentication |
| **Network Tools** | iputils, curl, wget, wget2, iproute2, iptables, libpcap, libnl, nghttp2, libssh, libidn2, libpsl | Network diagnostics, file download, traffic control |
| **Container/Virtualization** | podman, podmansh | Image management, container runtime, network configuration |
| **SSH Tools** | openssh, openssh-clients | Key generation, SSH connection, scp/sftp |
| **Version Control** | git | Repository initialization, branch operations, remote management |
| **Scripting/Languages** | python, perl, lua, tcl, bash, tcsh, expect, swig | Interpreter, modules, script execution |
| **Libraries/Runtime** | glibc, glib, libffi, libxml2, libxslt, libpng, pcre2, expat, icu4c, libarchive, boost, json-c, sqlite, popt, readline, slang, newt, gmp, mpfr, mpc, mpdecimal, isl, libunistring, libxcrypt, libeconf, libcap, libaio, libbpf, libedit, libevent, libmnl, libnfnetlink, libnetfilter_conntrack, libnftnl, libpwquality, libtirpc, libsodium, nghttp2, libmicrohttpd, xxhash, jitterentropy, libgpg-error, libpsl, publicsuffix-list, iso-codes, brotli, lz4, zstd | Shared library verification, headers, pkg-config |
| **Build/Packaging** | rpmbuild, rpm, pkgconf, debugedit, dwz, chrpath, patch, pyproject-rpm-macros, python-rpm-macros, python-srpm-macros, python-rpm-generators, perl-rpm-packaging, rpm-config-openruyi, setup, filesystem, config | RPM package building, debug info, macro configuration |
| **Display/Desktop** | sddm, weston, labwc, groff, texinfo, help2man, scdoc, xmlto, source-highlight | Display manager, Wayland compositor, documentation generation |
| **Test Frameworks** | atf, cmocka, dejagnu, kyua, lutok, beakerlib | Test libraries, test frameworks |
| **Other System Tools** | tmux, cloud-utils-growpart, procps-ng, psmisc, vim, less, bc, time, which, ed, fdupes, lzip, rsync, nfs-utils, cracklib, e2fsprogs, gdb, gdbm, gpm, kbd, lvm2, ncurses, nss, nss_wrapper, pam_wrapper, socket_wrapper, uid_wrapper, perl-Error, perl-Locale-gettext, systemtap, tzdata, unbound, ca-certificates, ca-certificates-mozilla, openruyi-release, linux-headers, pciutils, attr, acl, bash-completion, authselect, cpio, cryptsetup, dbus, dbus-broker, diffutils, elfutils, file, findutils, gawk, git, nghttp2, python-flit-core, python-lxml, python-packaging, python-pip, python-pyelftools, python-setuptools, python-wheel, re2c, scdoc, source-highlight, swig, uid_wrapper, xmlto, xxhash | Terminal multiplexer, partition resizing, process management, editor, date/time |

### 1.3 Test Case Execution Status

| Test Type | Suites | Cases | Status |
|-----------|:---:|:---:|:---:|
| Smoke | 100 | 100 | ✅ All Passed |
| Functional | 281 | 3,216 | ✅ All Passed (566 pkgs + 2,407 LTP + 211 kernel + 32 compiler) |
| Security | 113 | 113 | ✅ All Passed (98 CVE + 8 nmap + 7 openscap) |
| Compatibility | 188 | 188 | ✅ Passed (LTP POSIX) |
| Performance | 32 | 84 | Executed (11 unixbench + 53 mmtests + 5 iozone + 6 fio + 4 stream + 4 lmbench + 5 sysbench) |
| Reliability | 12 | 12 | Executed (6 trinity + 6 stress-ng) |
| Feature | 0 | 0 | 🆕 |
| **Total** | **726** | **3,708** | |

Detailed documentation:
- [Smoke Test Coverage](docs/coverage/smoke-coverage.md)
- [Functional Test Coverage](docs/coverage/functional-coverage.md)
- [Security Test Coverage](docs/coverage/security-coverage.md)
- [Compatibility Test Coverage](docs/coverage/compatibility-coverage.md)
- [Performance Test Coverage](docs/coverage/unixbench_results.md)

---

## 2. User Guide

See [User Guide](docs/user_guide.md) -- covers complete steps from cloning the repository and installing dependencies to running individual test cases, test suites, full test type runs, and all tests.

---

## 3. Development Guide

See [Development Guide](docs/development-guide.md) — covers how to add new test cases, directory conventions, BeakerLib lifecycle, FMF metadata specifications, and naming conventions.

See [CI Guide](docs/ci_guide.md) — covers CI/CD workflows, checkpoints, pool architecture, and test execution pipeline with Mermaid flowcharts.

---

## 4. Test Report Templates

See [Test Report Templates](docs/test_reports.md) -- covers test overview, suite/case/pass/fail/skip statistics tables for each test type.

---

## 5. License

openruyi-autotest is licensed under [Mulan Permissive Software License, Version 2 (Mulan PSL v2)](LICENSE).

CopyrightText (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
CopyrightText (C) 2026 openRuyi Project Contributors
