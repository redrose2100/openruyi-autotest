# openruyi-autotest

openruyi-autotest is an automated testing project based on the [tmt (Test Management Tool)](https://tmt.readthedocs.io/) framework, using [BeakerLib](https://github.com/beakerlib/beakerlib) for test scripts and [FMF](https://fmf.readthedocs.io/) for metadata management. It covers seven categories: Smoke, Functional, Security, Compatibility, Performance, Reliability, and Feature tests, totaling 726 test suites and 3,708 test cases (Functional: 281 suites / 3,216 cases — 566 pkgs + 2,407 LTP + 211 kernel + 32 compiler; Security: 113 suites / 113 cases — 98 CVE + 8 nmap + 7 openscap; Reliability: 12 suites / 12 cases — 6 trinity + 6 stress-ng).

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
| **Build Tools** | [gcc](docs/coverage/functional/pkgs/gcc.md), g++ (gxx), [clang](docs/coverage/functional/pkgs/clang.md), [cmake](docs/coverage/functional/pkgs/cmake.md), [make](docs/coverage/functional/pkgs/make.md), [binutils](docs/coverage/functional/pkgs/binutils.md), [autoconf](docs/coverage/functional/pkgs/autoconf.md), [automake](docs/coverage/functional/pkgs/automake.md), [bison](docs/coverage/functional/pkgs/bison.md), [flex](docs/coverage/functional/pkgs/flex.md), [meson](docs/coverage/functional/pkgs/meson.md), [ninja](docs/coverage/functional/pkgs/ninja.md) |
| **System Management** | [systemd](docs/coverage/functional/pkgs/systemd.md), [systemd-timesyncd](docs/coverage/functional/pkgs/systemd-timesyncd.md), [dbus](docs/coverage/functional/pkgs/dbus.md), [dbus-broker](docs/coverage/functional/pkgs/dbus-broker.md), [chkconfig](docs/coverage/functional/pkgs/chkconfig.md), [kmod](docs/coverage/functional/pkgs/kmod.md), [util-linux](docs/coverage/functional/pkgs/util-linux.md) |
| **File/Text Tools** | [coreutils](docs/coverage/functional/pkgs/coreutils.md), [tar](docs/coverage/functional/pkgs/tar.md), [grep](docs/coverage/functional/pkgs/grep.md), [sed](docs/coverage/functional/pkgs/sed.md), [gawk](docs/coverage/functional/pkgs/gawk.md), [diffutils](docs/coverage/functional/pkgs/diffutils.md), [findutils](docs/coverage/functional/pkgs/findutils.md), [file](docs/coverage/functional/pkgs/file.md), [gzip](docs/coverage/functional/pkgs/gzip.md), [xz](docs/coverage/functional/pkgs/xz.md), [zstd](docs/coverage/functional/pkgs/zstd.md), [bzip2](docs/coverage/functional/pkgs/bzip2.md), [lz4](docs/coverage/functional/pkgs/lz4.md), [unzip](docs/coverage/functional/pkgs/unzip.md), [cpio](docs/coverage/functional/pkgs/cpio.md), [dos2unix](docs/coverage/functional/pkgs/dos2unix.md) |
| **Security/Crypto** | [openssl](docs/coverage/functional/pkgs/openssl.md), [gnutls](docs/coverage/functional/pkgs/gnutls.md), [libgcrypt](docs/coverage/functional/pkgs/libgcrypt.md), [nettle](docs/coverage/functional/pkgs/nettle.md), [libtasn1](docs/coverage/functional/pkgs/libtasn1.md), [p11-kit](docs/coverage/functional/pkgs/p11-kit.md), [cryptsetup](docs/coverage/functional/pkgs/cryptsetup.md), [pam](docs/coverage/functional/pkgs/pam.md), [libselinux](docs/coverage/functional/pkgs/libselinux.md), [libseccomp](docs/coverage/functional/pkgs/libseccomp.md), [audit](docs/coverage/functional/pkgs/audit.md), [keyutils](docs/coverage/functional/pkgs/keyutils.md), [krb5](docs/coverage/functional/pkgs/krb5.md) |
| **Network Tools** | [iputils](docs/coverage/functional/pkgs/iputils.md), [curl](docs/coverage/functional/pkgs/curl.md), [wget](docs/coverage/functional/pkgs/wget.md), [wget2](docs/coverage/functional/pkgs/wget2.md), [iproute2](docs/coverage/functional/pkgs/iproute2.md), [iptables](docs/coverage/functional/pkgs/iptables.md), [libpcap](docs/coverage/functional/pkgs/libpcap.md), [libnl](docs/coverage/functional/pkgs/libnl.md), [nghttp2](docs/coverage/functional/pkgs/nghttp2.md), [libssh](docs/coverage/functional/pkgs/libssh.md), [libidn2](docs/coverage/functional/pkgs/libidn2.md), [libpsl](docs/coverage/functional/pkgs/libpsl.md) |
| **Container/Virtualization** | [podman](docs/coverage/functional/pkgs/podman.md), [podmansh](docs/coverage/functional/pkgs/podmansh.md) |
| **SSH Tools** | [openssh](docs/coverage/functional/pkgs/openssh.md), [openssh-clients](docs/coverage/functional/pkgs/openssh-clients.md) |
| **Version Control** | [git](docs/coverage/functional/pkgs/git.md) |
| **Scripting/Languages** | [python](docs/coverage/functional/pkgs/python.md), [perl](docs/coverage/functional/pkgs/perl.md), [lua](docs/coverage/functional/pkgs/lua.md), [tcl](docs/coverage/functional/pkgs/tcl.md), [bash](docs/coverage/functional/pkgs/bash.md), [tcsh](docs/coverage/functional/pkgs/tcsh.md), [expect](docs/coverage/functional/pkgs/expect.md), [swig](docs/coverage/functional/pkgs/swig.md) |
| **Libraries/Runtime** | [glibc](docs/coverage/functional/pkgs/glibc.md), [glib](docs/coverage/functional/pkgs/glib.md), [libffi](docs/coverage/functional/pkgs/libffi.md), [libxml2](docs/coverage/functional/pkgs/libxml2.md), [libxslt](docs/coverage/functional/pkgs/libxslt.md), [libpng](docs/coverage/functional/pkgs/libpng.md), [pcre2](docs/coverage/functional/pkgs/pcre2.md), [expat](docs/coverage/functional/pkgs/expat.md), [icu4c](docs/coverage/functional/pkgs/icu4c.md), [libarchive](docs/coverage/functional/pkgs/libarchive.md), [boost](docs/coverage/functional/pkgs/boost.md), [json-c](docs/coverage/functional/pkgs/json-c.md), [sqlite](docs/coverage/functional/pkgs/sqlite.md), [popt](docs/coverage/functional/pkgs/popt.md), [readline](docs/coverage/functional/pkgs/readline.md), [slang](docs/coverage/functional/pkgs/slang.md), [newt](docs/coverage/functional/pkgs/newt.md), [gmp](docs/coverage/functional/pkgs/gmp.md), [mpfr](docs/coverage/functional/pkgs/mpfr.md), [mpc](docs/coverage/functional/pkgs/mpc.md), [mpdecimal](docs/coverage/functional/pkgs/mpdecimal.md), [isl](docs/coverage/functional/pkgs/isl.md), [libunistring](docs/coverage/functional/pkgs/libunistring.md), [libxcrypt](docs/coverage/functional/pkgs/libxcrypt.md), [libeconf](docs/coverage/functional/pkgs/libeconf.md), [libcap](docs/coverage/functional/pkgs/libcap.md), [libaio](docs/coverage/functional/pkgs/libaio.md), [libbpf](docs/coverage/functional/pkgs/libbpf.md), [libedit](docs/coverage/functional/pkgs/libedit.md), [libevent](docs/coverage/functional/pkgs/libevent.md), [libmnl](docs/coverage/functional/pkgs/libmnl.md), [libnfnetlink](docs/coverage/functional/pkgs/libnfnetlink.md), [libnetfilter_conntrack](docs/coverage/functional/pkgs/libnetfilter_conntrack.md), [libnftnl](docs/coverage/functional/pkgs/libnftnl.md), [libpwquality](docs/coverage/functional/pkgs/libpwquality.md), [libtirpc](docs/coverage/functional/pkgs/libtirpc.md), [libsodium](docs/coverage/functional/pkgs/libsodium.md), [nghttp2](docs/coverage/functional/pkgs/nghttp2.md), [libmicrohttpd](docs/coverage/functional/pkgs/libmicrohttpd.md), [xxhash](docs/coverage/functional/pkgs/xxhash.md), [jitterentropy](docs/coverage/functional/pkgs/jitterentropy.md), [libgpg-error](docs/coverage/functional/pkgs/libgpg-error.md), [libpsl](docs/coverage/functional/pkgs/libpsl.md), [publicsuffix-list](docs/coverage/functional/pkgs/publicsuffix-list.md), [iso-codes](docs/coverage/functional/pkgs/iso-codes.md), [brotli](docs/coverage/functional/pkgs/brotli.md), [lz4](docs/coverage/functional/pkgs/lz4.md), [zstd](docs/coverage/functional/pkgs/zstd.md) |
| **Build/Packaging** | [rpmbuild](docs/coverage/functional/pkgs/rpmbuild.md), [rpm](docs/coverage/functional/pkgs/rpm.md), [pkgconf](docs/coverage/functional/pkgs/pkgconf.md), [debugedit](docs/coverage/functional/pkgs/debugedit.md), [dwz](docs/coverage/functional/pkgs/dwz.md), [chrpath](docs/coverage/functional/pkgs/chrpath.md), [patch](docs/coverage/functional/pkgs/patch.md), [pyproject-rpm-macros](docs/coverage/functional/pkgs/pyproject-rpm-macros.md), [python-rpm-macros](docs/coverage/functional/pkgs/python-rpm-macros.md), [python-srpm-macros](docs/coverage/functional/pkgs/python-srpm-macros.md), [python-rpm-generators](docs/coverage/functional/pkgs/python-rpm-generators.md), [perl-rpm-packaging](docs/coverage/functional/pkgs/perl-rpm-packaging.md), [rpm-config-openruyi](docs/coverage/functional/pkgs/rpm-config-openruyi.md), [setup](docs/coverage/functional/pkgs/setup.md), [filesystem](docs/coverage/functional/pkgs/filesystem.md), [config](docs/coverage/functional/pkgs/config.md) |
| **Display/Desktop** | [sddm](docs/coverage/functional/pkgs/sddm.md), [weston](docs/coverage/functional/pkgs/weston.md), [labwc](docs/coverage/functional/pkgs/labwc.md), [groff](docs/coverage/functional/pkgs/groff.md), [texinfo](docs/coverage/functional/pkgs/texinfo.md), [help2man](docs/coverage/functional/pkgs/help2man.md), [scdoc](docs/coverage/functional/pkgs/scdoc.md), [xmlto](docs/coverage/functional/pkgs/xmlto.md), [source-highlight](docs/coverage/functional/pkgs/source-highlight.md) |
| **Test Frameworks** | [atf](docs/coverage/functional/pkgs/atf.md), [cmocka](docs/coverage/functional/pkgs/cmocka.md), [dejagnu](docs/coverage/functional/pkgs/dejagnu.md), [kyua](docs/coverage/functional/pkgs/kyua.md), [lutok](docs/coverage/functional/pkgs/lutok.md), [beakerlib](docs/coverage/functional/pkgs/beakerlib.md) |
| **Other System Tools** | [tmux](docs/coverage/functional/pkgs/tmux.md), [cloud-utils-growpart](docs/coverage/functional/pkgs/cloud-utils-growpart.md), [procps-ng](docs/coverage/functional/pkgs/procps-ng.md), [psmisc](docs/coverage/functional/pkgs/psmisc.md), [vim](docs/coverage/functional/pkgs/vim.md), [less](docs/coverage/functional/pkgs/less.md), [bc](docs/coverage/functional/pkgs/bc.md), [time](docs/coverage/functional/pkgs/time.md), [which](docs/coverage/functional/pkgs/which.md), [ed](docs/coverage/functional/pkgs/ed.md), [fdupes](docs/coverage/functional/pkgs/fdupes.md), [lzip](docs/coverage/functional/pkgs/lzip.md), [rsync](docs/coverage/functional/pkgs/rsync.md), [nfs-utils](docs/coverage/functional/pkgs/nfs-utils.md), [cracklib](docs/coverage/functional/pkgs/cracklib.md), [e2fsprogs](docs/coverage/functional/pkgs/e2fsprogs.md), [gdb](docs/coverage/functional/pkgs/gdb.md), [gdbm](docs/coverage/functional/pkgs/gdbm.md), [gpm](docs/coverage/functional/pkgs/gpm.md), [kbd](docs/coverage/functional/pkgs/kbd.md), [lvm2](docs/coverage/functional/pkgs/lvm2.md), [ncurses](docs/coverage/functional/pkgs/ncurses.md), [nss](docs/coverage/functional/pkgs/nss.md), [nss_wrapper](docs/coverage/functional/pkgs/nss_wrapper.md), pam_wrapper, [socket_wrapper](docs/coverage/functional/pkgs/socket_wrapper.md), [uid_wrapper](docs/coverage/functional/pkgs/uid_wrapper.md), [perl-Error](docs/coverage/functional/pkgs/perl-Error.md), [perl-Locale-gettext](docs/coverage/functional/pkgs/perl-Locale-gettext.md), [systemtap](docs/coverage/functional/pkgs/systemtap.md), [tzdata](docs/coverage/functional/pkgs/tzdata.md), [unbound](docs/coverage/functional/pkgs/unbound.md), [ca-certificates](docs/coverage/functional/pkgs/ca-certificates.md), [ca-certificates-mozilla](docs/coverage/functional/pkgs/ca-certificates-mozilla.md), [openruyi-release](docs/coverage/functional/pkgs/openruyi-release.md), [linux-headers](docs/coverage/functional/pkgs/linux-headers.md), [pciutils](docs/coverage/functional/pkgs/pciutils.md), [attr](docs/coverage/functional/pkgs/attr.md), [acl](docs/coverage/functional/pkgs/acl.md), [bash-completion](docs/coverage/functional/pkgs/bash-completion.md), [authselect](docs/coverage/functional/pkgs/authselect.md), [cpio](docs/coverage/functional/pkgs/cpio.md), [cryptsetup](docs/coverage/functional/pkgs/cryptsetup.md), [dbus](docs/coverage/functional/pkgs/dbus.md), [dbus-broker](docs/coverage/functional/pkgs/dbus-broker.md), [diffutils](docs/coverage/functional/pkgs/diffutils.md), [elfutils](docs/coverage/functional/pkgs/elfutils.md), [file](docs/coverage/functional/pkgs/file.md), [findutils](docs/coverage/functional/pkgs/findutils.md), [gawk](docs/coverage/functional/pkgs/gawk.md), [git](docs/coverage/functional/pkgs/git.md), [nghttp2](docs/coverage/functional/pkgs/nghttp2.md), [python-flit-core](docs/coverage/functional/pkgs/python-flit-core.md), [python-lxml](docs/coverage/functional/pkgs/python-lxml.md), [python-packaging](docs/coverage/functional/pkgs/python-packaging.md), [python-pip](docs/coverage/functional/pkgs/python-pip.md), [python-pyelftools](docs/coverage/functional/pkgs/python-pyelftools.md), [python-setuptools](docs/coverage/functional/pkgs/python-setuptools.md), [python-wheel](docs/coverage/functional/pkgs/python-wheel.md), [re2c](docs/coverage/functional/pkgs/re2c.md), [scdoc](docs/coverage/functional/pkgs/scdoc.md), [source-highlight](docs/coverage/functional/pkgs/source-highlight.md), [swig](docs/coverage/functional/pkgs/swig.md), [uid_wrapper](docs/coverage/functional/pkgs/uid_wrapper.md), [xmlto](docs/coverage/functional/pkgs/xmlto.md), [xxhash](docs/coverage/functional/pkgs/xxhash.md) |

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
- [Functional Test Coverage](docs/coverage/functional/pkgs/index.md)
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
