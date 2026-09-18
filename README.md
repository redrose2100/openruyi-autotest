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

| Category | Representative Packages |
|----------|------------------------|
| **Build Tools** | [gcc](docs/coverage/functional-coverage/gcc.md), g++ (gxx), [clang](docs/coverage/functional-coverage/clang.md), [cmake](docs/coverage/functional-coverage/cmake.md), [make](docs/coverage/functional-coverage/make.md), [binutils](docs/coverage/functional-coverage/binutils.md), [autoconf](docs/coverage/functional-coverage/autoconf.md), [automake](docs/coverage/functional-coverage/automake.md), [bison](docs/coverage/functional-coverage/bison.md), [flex](docs/coverage/functional-coverage/flex.md), [meson](docs/coverage/functional-coverage/meson.md), [ninja](docs/coverage/functional-coverage/ninja.md) |
| **System Management** | [systemd](docs/coverage/functional-coverage/systemd.md), [systemd-timesyncd](docs/coverage/functional-coverage/systemd-timesyncd.md), [dbus](docs/coverage/functional-coverage/dbus.md), [dbus-broker](docs/coverage/functional-coverage/dbus-broker.md), [chkconfig](docs/coverage/functional-coverage/chkconfig.md), [kmod](docs/coverage/functional-coverage/kmod.md), [util-linux](docs/coverage/functional-coverage/util-linux.md) |
| **File/Text Tools** | [coreutils](docs/coverage/functional-coverage/coreutils.md), [tar](docs/coverage/functional-coverage/tar.md), [grep](docs/coverage/functional-coverage/grep.md), [sed](docs/coverage/functional-coverage/sed.md), [gawk](docs/coverage/functional-coverage/gawk.md), [diffutils](docs/coverage/functional-coverage/diffutils.md), [findutils](docs/coverage/functional-coverage/findutils.md), [file](docs/coverage/functional-coverage/file.md), [gzip](docs/coverage/functional-coverage/gzip.md), [xz](docs/coverage/functional-coverage/xz.md), [zstd](docs/coverage/functional-coverage/zstd.md), [bzip2](docs/coverage/functional-coverage/bzip2.md), [lz4](docs/coverage/functional-coverage/lz4.md), [unzip](docs/coverage/functional-coverage/unzip.md), [cpio](docs/coverage/functional-coverage/cpio.md), [dos2unix](docs/coverage/functional-coverage/dos2unix.md) |
| **Security/Crypto** | [openssl](docs/coverage/functional-coverage/openssl.md), [gnutls](docs/coverage/functional-coverage/gnutls.md), [libgcrypt](docs/coverage/functional-coverage/libgcrypt.md), [nettle](docs/coverage/functional-coverage/nettle.md), [libtasn1](docs/coverage/functional-coverage/libtasn1.md), [p11-kit](docs/coverage/functional-coverage/p11-kit.md), [cryptsetup](docs/coverage/functional-coverage/cryptsetup.md), [pam](docs/coverage/functional-coverage/pam.md), [libselinux](docs/coverage/functional-coverage/libselinux.md), [libseccomp](docs/coverage/functional-coverage/libseccomp.md), [audit](docs/coverage/functional-coverage/audit.md), [keyutils](docs/coverage/functional-coverage/keyutils.md), [krb5](docs/coverage/functional-coverage/krb5.md) |
| **Network Tools** | [iputils](docs/coverage/functional-coverage/iputils.md), [curl](docs/coverage/functional-coverage/curl.md), [wget](docs/coverage/functional-coverage/wget.md), [wget2](docs/coverage/functional-coverage/wget2.md), [iproute2](docs/coverage/functional-coverage/iproute2.md), [iptables](docs/coverage/functional-coverage/iptables.md), [libpcap](docs/coverage/functional-coverage/libpcap.md), [libnl](docs/coverage/functional-coverage/libnl.md), [nghttp2](docs/coverage/functional-coverage/nghttp2.md), [libssh](docs/coverage/functional-coverage/libssh.md), [libidn2](docs/coverage/functional-coverage/libidn2.md), [libpsl](docs/coverage/functional-coverage/libpsl.md) |
| **Container/Virtualization** | [podman](docs/coverage/functional-coverage/podman.md), [podmansh](docs/coverage/functional-coverage/podmansh.md) |
| **SSH Tools** | [openssh](docs/coverage/functional-coverage/openssh.md), [openssh-clients](docs/coverage/functional-coverage/openssh-clients.md) |
| **Version Control** | [git](docs/coverage/functional-coverage/git.md) |
| **Scripting/Languages** | [python](docs/coverage/functional-coverage/python.md), [perl](docs/coverage/functional-coverage/perl.md), [lua](docs/coverage/functional-coverage/lua.md), [tcl](docs/coverage/functional-coverage/tcl.md), [bash](docs/coverage/functional-coverage/bash.md), [tcsh](docs/coverage/functional-coverage/tcsh.md), [expect](docs/coverage/functional-coverage/expect.md), [swig](docs/coverage/functional-coverage/swig.md) |
| **Libraries/Runtime** | [glibc](docs/coverage/functional-coverage/glibc.md), [glib](docs/coverage/functional-coverage/glib.md), [libffi](docs/coverage/functional-coverage/libffi.md), [libxml2](docs/coverage/functional-coverage/libxml2.md), [libxslt](docs/coverage/functional-coverage/libxslt.md), [libpng](docs/coverage/functional-coverage/libpng.md), [pcre2](docs/coverage/functional-coverage/pcre2.md), [expat](docs/coverage/functional-coverage/expat.md), [icu4c](docs/coverage/functional-coverage/icu4c.md), [libarchive](docs/coverage/functional-coverage/libarchive.md), [boost](docs/coverage/functional-coverage/boost.md), [json-c](docs/coverage/functional-coverage/json-c.md), [sqlite](docs/coverage/functional-coverage/sqlite.md), [popt](docs/coverage/functional-coverage/popt.md), [readline](docs/coverage/functional-coverage/readline.md), [slang](docs/coverage/functional-coverage/slang.md), [newt](docs/coverage/functional-coverage/newt.md), [gmp](docs/coverage/functional-coverage/gmp.md), [mpfr](docs/coverage/functional-coverage/mpfr.md), [mpc](docs/coverage/functional-coverage/mpc.md), [mpdecimal](docs/coverage/functional-coverage/mpdecimal.md), [isl](docs/coverage/functional-coverage/isl.md), [libunistring](docs/coverage/functional-coverage/libunistring.md), [libxcrypt](docs/coverage/functional-coverage/libxcrypt.md), [libeconf](docs/coverage/functional-coverage/libeconf.md), [libcap](docs/coverage/functional-coverage/libcap.md), [libaio](docs/coverage/functional-coverage/libaio.md), [libbpf](docs/coverage/functional-coverage/libbpf.md), [libedit](docs/coverage/functional-coverage/libedit.md), [libevent](docs/coverage/functional-coverage/libevent.md), [libmnl](docs/coverage/functional-coverage/libmnl.md), [libnfnetlink](docs/coverage/functional-coverage/libnfnetlink.md), [libnetfilter_conntrack](docs/coverage/functional-coverage/libnetfilter_conntrack.md), [libnftnl](docs/coverage/functional-coverage/libnftnl.md), [libpwquality](docs/coverage/functional-coverage/libpwquality.md), [libtirpc](docs/coverage/functional-coverage/libtirpc.md), [libsodium](docs/coverage/functional-coverage/libsodium.md), [nghttp2](docs/coverage/functional-coverage/nghttp2.md), [libmicrohttpd](docs/coverage/functional-coverage/libmicrohttpd.md), [xxhash](docs/coverage/functional-coverage/xxhash.md), [jitterentropy](docs/coverage/functional-coverage/jitterentropy.md), [libgpg-error](docs/coverage/functional-coverage/libgpg-error.md), [libpsl](docs/coverage/functional-coverage/libpsl.md), [publicsuffix-list](docs/coverage/functional-coverage/publicsuffix-list.md), [iso-codes](docs/coverage/functional-coverage/iso-codes.md), [brotli](docs/coverage/functional-coverage/brotli.md), [lz4](docs/coverage/functional-coverage/lz4.md), [zstd](docs/coverage/functional-coverage/zstd.md) |
| **Build/Packaging** | [rpmbuild](docs/coverage/functional-coverage/rpmbuild.md), [rpm](docs/coverage/functional-coverage/rpm.md), [pkgconf](docs/coverage/functional-coverage/pkgconf.md), [debugedit](docs/coverage/functional-coverage/debugedit.md), [dwz](docs/coverage/functional-coverage/dwz.md), [chrpath](docs/coverage/functional-coverage/chrpath.md), [patch](docs/coverage/functional-coverage/patch.md), [pyproject-rpm-macros](docs/coverage/functional-coverage/pyproject-rpm-macros.md), [python-rpm-macros](docs/coverage/functional-coverage/python-rpm-macros.md), [python-srpm-macros](docs/coverage/functional-coverage/python-srpm-macros.md), [python-rpm-generators](docs/coverage/functional-coverage/python-rpm-generators.md), [perl-rpm-packaging](docs/coverage/functional-coverage/perl-rpm-packaging.md), [rpm-config-openruyi](docs/coverage/functional-coverage/rpm-config-openruyi.md), [setup](docs/coverage/functional-coverage/setup.md), [filesystem](docs/coverage/functional-coverage/filesystem.md), [config](docs/coverage/functional-coverage/config.md) |
| **Display/Desktop** | [sddm](docs/coverage/functional-coverage/sddm.md), [weston](docs/coverage/functional-coverage/weston.md), [labwc](docs/coverage/functional-coverage/labwc.md), [groff](docs/coverage/functional-coverage/groff.md), [texinfo](docs/coverage/functional-coverage/texinfo.md), [help2man](docs/coverage/functional-coverage/help2man.md), [scdoc](docs/coverage/functional-coverage/scdoc.md), [xmlto](docs/coverage/functional-coverage/xmlto.md), [source-highlight](docs/coverage/functional-coverage/source-highlight.md) |
| **Test Frameworks** | [atf](docs/coverage/functional-coverage/atf.md), [cmocka](docs/coverage/functional-coverage/cmocka.md), [dejagnu](docs/coverage/functional-coverage/dejagnu.md), [kyua](docs/coverage/functional-coverage/kyua.md), [lutok](docs/coverage/functional-coverage/lutok.md), [beakerlib](docs/coverage/functional-coverage/beakerlib.md) |
| **Other System Tools** | [tmux](docs/coverage/functional-coverage/tmux.md), [cloud-utils-growpart](docs/coverage/functional-coverage/cloud-utils-growpart.md), [procps-ng](docs/coverage/functional-coverage/procps-ng.md), [psmisc](docs/coverage/functional-coverage/psmisc.md), [vim](docs/coverage/functional-coverage/vim.md), [less](docs/coverage/functional-coverage/less.md), [bc](docs/coverage/functional-coverage/bc.md), [time](docs/coverage/functional-coverage/time.md), [which](docs/coverage/functional-coverage/which.md), [ed](docs/coverage/functional-coverage/ed.md), [fdupes](docs/coverage/functional-coverage/fdupes.md), [lzip](docs/coverage/functional-coverage/lzip.md), [rsync](docs/coverage/functional-coverage/rsync.md), [nfs-utils](docs/coverage/functional-coverage/nfs-utils.md), [cracklib](docs/coverage/functional-coverage/cracklib.md), [e2fsprogs](docs/coverage/functional-coverage/e2fsprogs.md), [gdb](docs/coverage/functional-coverage/gdb.md), [gdbm](docs/coverage/functional-coverage/gdbm.md), [gpm](docs/coverage/functional-coverage/gpm.md), [kbd](docs/coverage/functional-coverage/kbd.md), [lvm2](docs/coverage/functional-coverage/lvm2.md), [ncurses](docs/coverage/functional-coverage/ncurses.md), [nss](docs/coverage/functional-coverage/nss.md), [nss_wrapper](docs/coverage/functional-coverage/nss_wrapper.md), pam_wrapper, [socket_wrapper](docs/coverage/functional-coverage/socket_wrapper.md), [uid_wrapper](docs/coverage/functional-coverage/uid_wrapper.md), [perl-Error](docs/coverage/functional-coverage/perl-Error.md), [perl-Locale-gettext](docs/coverage/functional-coverage/perl-Locale-gettext.md), [systemtap](docs/coverage/functional-coverage/systemtap.md), [tzdata](docs/coverage/functional-coverage/tzdata.md), [unbound](docs/coverage/functional-coverage/unbound.md), [ca-certificates](docs/coverage/functional-coverage/ca-certificates.md), [ca-certificates-mozilla](docs/coverage/functional-coverage/ca-certificates-mozilla.md), [openruyi-release](docs/coverage/functional-coverage/openruyi-release.md), [linux-headers](docs/coverage/functional-coverage/linux-headers.md), [pciutils](docs/coverage/functional-coverage/pciutils.md), [attr](docs/coverage/functional-coverage/attr.md), [acl](docs/coverage/functional-coverage/acl.md), [bash-completion](docs/coverage/functional-coverage/bash-completion.md), [authselect](docs/coverage/functional-coverage/authselect.md), [cpio](docs/coverage/functional-coverage/cpio.md), [cryptsetup](docs/coverage/functional-coverage/cryptsetup.md), [dbus](docs/coverage/functional-coverage/dbus.md), [dbus-broker](docs/coverage/functional-coverage/dbus-broker.md), [diffutils](docs/coverage/functional-coverage/diffutils.md), [elfutils](docs/coverage/functional-coverage/elfutils.md), [file](docs/coverage/functional-coverage/file.md), [findutils](docs/coverage/functional-coverage/findutils.md), [gawk](docs/coverage/functional-coverage/gawk.md), [git](docs/coverage/functional-coverage/git.md), [nghttp2](docs/coverage/functional-coverage/nghttp2.md), [python-flit-core](docs/coverage/functional-coverage/python-flit-core.md), [python-lxml](docs/coverage/functional-coverage/python-lxml.md), [python-packaging](docs/coverage/functional-coverage/python-packaging.md), [python-pip](docs/coverage/functional-coverage/python-pip.md), [python-pyelftools](docs/coverage/functional-coverage/python-pyelftools.md), [python-setuptools](docs/coverage/functional-coverage/python-setuptools.md), [python-wheel](docs/coverage/functional-coverage/python-wheel.md), [re2c](docs/coverage/functional-coverage/re2c.md), [scdoc](docs/coverage/functional-coverage/scdoc.md), [source-highlight](docs/coverage/functional-coverage/source-highlight.md), [swig](docs/coverage/functional-coverage/swig.md), [uid_wrapper](docs/coverage/functional-coverage/uid_wrapper.md), [xmlto](docs/coverage/functional-coverage/xmlto.md), [xxhash](docs/coverage/functional-coverage/xxhash.md) |

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
- [Functional Test Coverage](docs/coverage/functional-coverage/index.md)
- [Security Test Coverage](docs/coverage/security-coverage.md)
- [Compatibility Test Coverage](docs/coverage/compatibility-coverage.md)
- [Performance Test Coverage](docs/coverage/unixbench_results.md)

---

## 2. User Guide

See [User Guide](docs/user_guide.md) -- covers complete steps from cloning the repository and installing dependencies to running individual test cases, test suites, full test type runs, and all tests.

---

## 3. Development Guide

See [Development Guide](docs/development-guide.md) -- covers how to add new test cases, directory conventions, BeakerLib lifecycle, FMF metadata specifications, and naming conventions.

---

## 4. Test Report Templates

See [Test Report Templates](docs/test_reports.md) -- covers test overview, suite/case/pass/fail/skip statistics tables for each test type.

---

## 5. License

openruyi-autotest is licensed under [Mulan Permissive Software License, Version 2 (Mulan PSL v2)](LICENSE).

CopyrightText (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
CopyrightText (C) 2026 openRuyi Project Contributors
