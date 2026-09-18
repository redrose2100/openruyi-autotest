# openruyi-autotest

openruyi-autotest 是基于 [tmt (Test Management Tool)](https://tmt.readthedocs.io/) 框架的自动化测试项目，使用 [BeakerLib](https://github.com/beakerlib/beakerlib) 编写测试脚本，通过 [FMF](https://fmf.readthedocs.io/) 管理元数据。涵盖冒烟测试、功能测试、安全测试、兼容性测试、性能测试、可靠性测试和特性测试七大类，共 726 个测试套、3708 个测试用例（功能测试 281 套 / 3216 用例：566 pkgs + 2407 LTP + 211 kernel + 32 compiler；安全测试 113 套 / 113 用例：98 CVE + 8 nmap + 7 openscap；可靠性测试 12 套 / 12 用例：6 trinity + 6 stress-ng）。

> :us: [English Version (英文版)](README.md)

---

## 一、openruyi-autotest 简介

### 1.1 目录结构

```
openruyi-autotest/
├── .fmf/                        # FMF 元数据根目录
│   └── version
├── plans/                       # 测试计划
│   ├── smoke.fmf                 # 冒烟测试计划
│   ├── functional.fmf            # 功能测试计划
│   ├── security.fmf              # 安全测试计划
│   ├── compatibility.fmf         # 兼容性测试计划
│   ├── performance.fmf           # 性能测试计划
│   ├── reliability.fmf           # 可靠性测试计划
│   ├── feature.fmf               # 特性测试计划
│   └── all.fmf                   # 全量测试计划
├── tests/                       # 测试用例
│   ├── main.fmf                  # 全局共享配置
│   ├── smoke/                    # 冒烟测试（100 个用例）
│   ├── functional/               # 功能测试
│   │   ├── kernel/               # 内核功能测试
│   │   │   ├── blktests/         #   块设备测试（195 个用例）
│   │   │   └── realtime/         #   实时性测试（16 个用例）
│   │   ├── ltp/                  # LTP 功能测试套件（32 个子模块, 2407 个用例）
│   │   ├── pkgs/                 # RPM 软件包功能测试（202 个包, 566 个用例）
│   │   └── compiler/             # 编译器与工具链测试（32 个用例）
│   │       ├── dejagnu/          #   DejaGnu GCC 测试框架（9 个用例）
│   │       ├── jotai/            #   Jotai 基准程序测试（7 个用例）
│   │       ├── csmith/           #   Csmith 随机程序差分测试（8 个用例）
│   │       └── yarpgen/          #   YARPGen 优化 Bug 检测（8 个用例）
│   ├── security/                 # 安全测试（113 个用例）
│   │   ├── cve/                  # CVE 漏洞测试（98 个用例）
│   │   ├── nmap/                 # 网络扫描测试（8 个用例）
│   │   ├── openscap/             # 安全合规性测试（7 个用例：4 基础 + 3 CIS）
│   │   │   ├── basic/             #   基础 CLI 操作（4 个用例）
│   │   │   └── cis/               #   CIS Benchmark（3 个用例）
│   ├── compatibility/            # 兼容性测试（188 个用例）
│   ├── performance/              # 性能测试
│   │   ├── mmtests/              #   MMTests 基准测试（53 个用例）
│   │   ├── unixbench/            #   UnixBench 基准测试（11 个用例）
│   │   ├── iozone/               #   IOzone 文件系统 I/O 基准（5 个用例）
│   │   ├── fio/                  #   fio 存储 I/O 性能测试（6 个用例）
│   │   ├── stream/               #   STREAM 内存带宽基准（4 个用例）
│   │   ├── lmbench/              #   LMbench 微基准测试（4 个用例）
│   │   └── sysbench/             #   sysbench 多线程基准（5 个用例）
│   ├── feature/                  # 特性测试
│   └── reliability/              # 可靠性测试
│       ├── trinity/              #   Trinity 系统调用 Fuzzer（6 个用例）
│       └── stress-ng/            #   stress-ng 系统压力测试（6 个用例）
├── docs/                        # 文档
└── README.md
```

### 1.2 测试覆盖详情

| 分类 | 代表性软件包 |
|----------|------------------------|
| **编译工具** | [gcc](docs/coverage/functional-coverage/gcc.md), g++ (gxx), [clang](docs/coverage/functional-coverage/clang.md), [cmake](docs/coverage/functional-coverage/cmake.md), [make](docs/coverage/functional-coverage/make.md), [binutils](docs/coverage/functional-coverage/binutils.md), [autoconf](docs/coverage/functional-coverage/autoconf.md), [automake](docs/coverage/functional-coverage/automake.md), [bison](docs/coverage/functional-coverage/bison.md), [flex](docs/coverage/functional-coverage/flex.md), [meson](docs/coverage/functional-coverage/meson.md), [ninja](docs/coverage/functional-coverage/ninja.md) |
| **系统管理** | [systemd](docs/coverage/functional-coverage/systemd.md), [systemd-timesyncd](docs/coverage/functional-coverage/systemd-timesyncd.md), [dbus](docs/coverage/functional-coverage/dbus.md), [dbus-broker](docs/coverage/functional-coverage/dbus-broker.md), [chkconfig](docs/coverage/functional-coverage/chkconfig.md), [kmod](docs/coverage/functional-coverage/kmod.md), [util-linux](docs/coverage/functional-coverage/util-linux.md) |
| **文件/文本工具** | [coreutils](docs/coverage/functional-coverage/coreutils.md), [tar](docs/coverage/functional-coverage/tar.md), [grep](docs/coverage/functional-coverage/grep.md), [sed](docs/coverage/functional-coverage/sed.md), [gawk](docs/coverage/functional-coverage/gawk.md), [diffutils](docs/coverage/functional-coverage/diffutils.md), [findutils](docs/coverage/functional-coverage/findutils.md), [file](docs/coverage/functional-coverage/file.md), [gzip](docs/coverage/functional-coverage/gzip.md), [xz](docs/coverage/functional-coverage/xz.md), [zstd](docs/coverage/functional-coverage/zstd.md), [bzip2](docs/coverage/functional-coverage/bzip2.md), [lz4](docs/coverage/functional-coverage/lz4.md), [unzip](docs/coverage/functional-coverage/unzip.md), [cpio](docs/coverage/functional-coverage/cpio.md), [dos2unix](docs/coverage/functional-coverage/dos2unix.md) |
| **安全/加密** | [openssl](docs/coverage/functional-coverage/openssl.md), [gnutls](docs/coverage/functional-coverage/gnutls.md), [libgcrypt](docs/coverage/functional-coverage/libgcrypt.md), [nettle](docs/coverage/functional-coverage/nettle.md), [libtasn1](docs/coverage/functional-coverage/libtasn1.md), [p11-kit](docs/coverage/functional-coverage/p11-kit.md), [cryptsetup](docs/coverage/functional-coverage/cryptsetup.md), [pam](docs/coverage/functional-coverage/pam.md), [libselinux](docs/coverage/functional-coverage/libselinux.md), [libseccomp](docs/coverage/functional-coverage/libseccomp.md), [audit](docs/coverage/functional-coverage/audit.md), [keyutils](docs/coverage/functional-coverage/keyutils.md), [krb5](docs/coverage/functional-coverage/krb5.md) |
| **网络工具** | [iputils](docs/coverage/functional-coverage/iputils.md), [curl](docs/coverage/functional-coverage/curl.md), [wget](docs/coverage/functional-coverage/wget.md), [wget2](docs/coverage/functional-coverage/wget2.md), [iproute2](docs/coverage/functional-coverage/iproute2.md), [iptables](docs/coverage/functional-coverage/iptables.md), [libpcap](docs/coverage/functional-coverage/libpcap.md), [libnl](docs/coverage/functional-coverage/libnl.md), [nghttp2](docs/coverage/functional-coverage/nghttp2.md), [libssh](docs/coverage/functional-coverage/libssh.md), [libidn2](docs/coverage/functional-coverage/libidn2.md), [libpsl](docs/coverage/functional-coverage/libpsl.md) |
| **容器/虚拟化** | [podman](docs/coverage/functional-coverage/podman.md), [podmansh](docs/coverage/functional-coverage/podmansh.md) |
| **SSH 工具** | [openssh](docs/coverage/functional-coverage/openssh.md), [openssh-clients](docs/coverage/functional-coverage/openssh-clients.md) |
| **版本控制** | [git](docs/coverage/functional-coverage/git.md) |
| **脚本/编程语言** | [python](docs/coverage/functional-coverage/python.md), [perl](docs/coverage/functional-coverage/perl.md), [lua](docs/coverage/functional-coverage/lua.md), [tcl](docs/coverage/functional-coverage/tcl.md), [bash](docs/coverage/functional-coverage/bash.md), [tcsh](docs/coverage/functional-coverage/tcsh.md), [expect](docs/coverage/functional-coverage/expect.md), [swig](docs/coverage/functional-coverage/swig.md) |
| **库/运行时** | [glibc](docs/coverage/functional-coverage/glibc.md), [glib](docs/coverage/functional-coverage/glib.md), [libffi](docs/coverage/functional-coverage/libffi.md), [libxml2](docs/coverage/functional-coverage/libxml2.md), [libxslt](docs/coverage/functional-coverage/libxslt.md), [libpng](docs/coverage/functional-coverage/libpng.md), [pcre2](docs/coverage/functional-coverage/pcre2.md), [expat](docs/coverage/functional-coverage/expat.md), [icu4c](docs/coverage/functional-coverage/icu4c.md), [libarchive](docs/coverage/functional-coverage/libarchive.md), [boost](docs/coverage/functional-coverage/boost.md), [json-c](docs/coverage/functional-coverage/json-c.md), [sqlite](docs/coverage/functional-coverage/sqlite.md), [popt](docs/coverage/functional-coverage/popt.md), [readline](docs/coverage/functional-coverage/readline.md), [slang](docs/coverage/functional-coverage/slang.md), [newt](docs/coverage/functional-coverage/newt.md), [gmp](docs/coverage/functional-coverage/gmp.md), [mpfr](docs/coverage/functional-coverage/mpfr.md), [mpc](docs/coverage/functional-coverage/mpc.md), [mpdecimal](docs/coverage/functional-coverage/mpdecimal.md), [isl](docs/coverage/functional-coverage/isl.md), [libunistring](docs/coverage/functional-coverage/libunistring.md), [libxcrypt](docs/coverage/functional-coverage/libxcrypt.md), [libeconf](docs/coverage/functional-coverage/libeconf.md), [libcap](docs/coverage/functional-coverage/libcap.md), [libaio](docs/coverage/functional-coverage/libaio.md), [libbpf](docs/coverage/functional-coverage/libbpf.md), [libedit](docs/coverage/functional-coverage/libedit.md), [libevent](docs/coverage/functional-coverage/libevent.md), [libmnl](docs/coverage/functional-coverage/libmnl.md), [libnfnetlink](docs/coverage/functional-coverage/libnfnetlink.md), [libnetfilter_conntrack](docs/coverage/functional-coverage/libnetfilter_conntrack.md), [libnftnl](docs/coverage/functional-coverage/libnftnl.md), [libpwquality](docs/coverage/functional-coverage/libpwquality.md), [libtirpc](docs/coverage/functional-coverage/libtirpc.md), [libsodium](docs/coverage/functional-coverage/libsodium.md), [nghttp2](docs/coverage/functional-coverage/nghttp2.md), [libmicrohttpd](docs/coverage/functional-coverage/libmicrohttpd.md), [xxhash](docs/coverage/functional-coverage/xxhash.md), [jitterentropy](docs/coverage/functional-coverage/jitterentropy.md), [libgpg-error](docs/coverage/functional-coverage/libgpg-error.md), [libpsl](docs/coverage/functional-coverage/libpsl.md), [publicsuffix-list](docs/coverage/functional-coverage/publicsuffix-list.md), [iso-codes](docs/coverage/functional-coverage/iso-codes.md), [brotli](docs/coverage/functional-coverage/brotli.md), [lz4](docs/coverage/functional-coverage/lz4.md), [zstd](docs/coverage/functional-coverage/zstd.md) |
| **构建/打包工具** | [rpmbuild](docs/coverage/functional-coverage/rpmbuild.md), [rpm](docs/coverage/functional-coverage/rpm.md), [pkgconf](docs/coverage/functional-coverage/pkgconf.md), [debugedit](docs/coverage/functional-coverage/debugedit.md), [dwz](docs/coverage/functional-coverage/dwz.md), [chrpath](docs/coverage/functional-coverage/chrpath.md), [patch](docs/coverage/functional-coverage/patch.md), [pyproject-rpm-macros](docs/coverage/functional-coverage/pyproject-rpm-macros.md), [python-rpm-macros](docs/coverage/functional-coverage/python-rpm-macros.md), [python-srpm-macros](docs/coverage/functional-coverage/python-srpm-macros.md), [python-rpm-generators](docs/coverage/functional-coverage/python-rpm-generators.md), [perl-rpm-packaging](docs/coverage/functional-coverage/perl-rpm-packaging.md), [rpm-config-openruyi](docs/coverage/functional-coverage/rpm-config-openruyi.md), [setup](docs/coverage/functional-coverage/setup.md), [filesystem](docs/coverage/functional-coverage/filesystem.md), [config](docs/coverage/functional-coverage/config.md) |
| **显示/桌面** | [sddm](docs/coverage/functional-coverage/sddm.md), [weston](docs/coverage/functional-coverage/weston.md), [labwc](docs/coverage/functional-coverage/labwc.md), [groff](docs/coverage/functional-coverage/groff.md), [texinfo](docs/coverage/functional-coverage/texinfo.md), [help2man](docs/coverage/functional-coverage/help2man.md), [scdoc](docs/coverage/functional-coverage/scdoc.md), [xmlto](docs/coverage/functional-coverage/xmlto.md), [source-highlight](docs/coverage/functional-coverage/source-highlight.md) |
| **测试框架** | [atf](docs/coverage/functional-coverage/atf.md), [cmocka](docs/coverage/functional-coverage/cmocka.md), [dejagnu](docs/coverage/functional-coverage/dejagnu.md), [kyua](docs/coverage/functional-coverage/kyua.md), [lutok](docs/coverage/functional-coverage/lutok.md), [beakerlib](docs/coverage/functional-coverage/beakerlib.md) |
| **其他系统工具** | [tmux](docs/coverage/functional-coverage/tmux.md), [cloud-utils-growpart](docs/coverage/functional-coverage/cloud-utils-growpart.md), [procps-ng](docs/coverage/functional-coverage/procps-ng.md), [psmisc](docs/coverage/functional-coverage/psmisc.md), [vim](docs/coverage/functional-coverage/vim.md), [less](docs/coverage/functional-coverage/less.md), [bc](docs/coverage/functional-coverage/bc.md), [time](docs/coverage/functional-coverage/time.md), [which](docs/coverage/functional-coverage/which.md), [ed](docs/coverage/functional-coverage/ed.md), [fdupes](docs/coverage/functional-coverage/fdupes.md), [lzip](docs/coverage/functional-coverage/lzip.md), [rsync](docs/coverage/functional-coverage/rsync.md), [nfs-utils](docs/coverage/functional-coverage/nfs-utils.md), [cracklib](docs/coverage/functional-coverage/cracklib.md), [e2fsprogs](docs/coverage/functional-coverage/e2fsprogs.md), [gdb](docs/coverage/functional-coverage/gdb.md), [gdbm](docs/coverage/functional-coverage/gdbm.md), [gpm](docs/coverage/functional-coverage/gpm.md), [kbd](docs/coverage/functional-coverage/kbd.md), [lvm2](docs/coverage/functional-coverage/lvm2.md), [ncurses](docs/coverage/functional-coverage/ncurses.md), [nss](docs/coverage/functional-coverage/nss.md), [nss_wrapper](docs/coverage/functional-coverage/nss_wrapper.md), pam_wrapper, [socket_wrapper](docs/coverage/functional-coverage/socket_wrapper.md), [uid_wrapper](docs/coverage/functional-coverage/uid_wrapper.md), [perl-Error](docs/coverage/functional-coverage/perl-Error.md), [perl-Locale-gettext](docs/coverage/functional-coverage/perl-Locale-gettext.md), [systemtap](docs/coverage/functional-coverage/systemtap.md), [tzdata](docs/coverage/functional-coverage/tzdata.md), [unbound](docs/coverage/functional-coverage/unbound.md), [ca-certificates](docs/coverage/functional-coverage/ca-certificates.md), [ca-certificates-mozilla](docs/coverage/functional-coverage/ca-certificates-mozilla.md), [openruyi-release](docs/coverage/functional-coverage/openruyi-release.md), [linux-headers](docs/coverage/functional-coverage/linux-headers.md), [pciutils](docs/coverage/functional-coverage/pciutils.md), [attr](docs/coverage/functional-coverage/attr.md), [acl](docs/coverage/functional-coverage/acl.md), [bash-completion](docs/coverage/functional-coverage/bash-completion.md), [authselect](docs/coverage/functional-coverage/authselect.md), [cpio](docs/coverage/functional-coverage/cpio.md), [cryptsetup](docs/coverage/functional-coverage/cryptsetup.md), [dbus](docs/coverage/functional-coverage/dbus.md), [dbus-broker](docs/coverage/functional-coverage/dbus-broker.md), [diffutils](docs/coverage/functional-coverage/diffutils.md), [elfutils](docs/coverage/functional-coverage/elfutils.md), [file](docs/coverage/functional-coverage/file.md), [findutils](docs/coverage/functional-coverage/findutils.md), [gawk](docs/coverage/functional-coverage/gawk.md), [git](docs/coverage/functional-coverage/git.md), [nghttp2](docs/coverage/functional-coverage/nghttp2.md), [python-flit-core](docs/coverage/functional-coverage/python-flit-core.md), [python-lxml](docs/coverage/functional-coverage/python-lxml.md), [python-packaging](docs/coverage/functional-coverage/python-packaging.md), [python-pip](docs/coverage/functional-coverage/python-pip.md), [python-pyelftools](docs/coverage/functional-coverage/python-pyelftools.md), [python-setuptools](docs/coverage/functional-coverage/python-setuptools.md), [python-wheel](docs/coverage/functional-coverage/python-wheel.md), [re2c](docs/coverage/functional-coverage/re2c.md), [scdoc](docs/coverage/functional-coverage/scdoc.md), [source-highlight](docs/coverage/functional-coverage/source-highlight.md), [swig](docs/coverage/functional-coverage/swig.md), [uid_wrapper](docs/coverage/functional-coverage/uid_wrapper.md), [xmlto](docs/coverage/functional-coverage/xmlto.md), [xxhash](docs/coverage/functional-coverage/xxhash.md) |

### 1.3 用例运行状态统计

| 测试类型 | 测试套数 | 用例数 | 状态 |
|---------|:---:|:---:|:---:|
| Smoke | 100 | 100 | ✅ 全部通过 |
| Functional | 281 | 3216 | ✅ 全部通过 (566 pkgs + 2407 LTP + 211 kernel + 32 compiler) |
| Security | 113 | 113 | ✅ 全部通过 (98 CVE + 8 nmap + 7 openscap) |
| Compatibility | 188 | 188 | ✅ 通过 (LTP POSIX) |
| Performance | 32 | 84 | 已执行 (11 unixbench + 53 mmtests + 5 iozone + 6 fio + 4 stream + 4 lmbench + 5 sysbench) |
| Reliability | 12 | 12 | 已执行 (6 trinity + 6 stress-ng) |
| Feature | 0 | 0 | 🆕 |
| **合计** | **726** | **3708** | |

详情文档：
- [冒烟测试覆盖详情](docs/coverage/smoke-coverage.md)
- [功能测试覆盖详情](docs/coverage/functional-coverage/index.md)
- [安全测试覆盖详情](docs/coverage/security-coverage.md)
- [兼容性测试覆盖详情](docs/coverage/compatibility-coverage.md)
- [性能测试覆盖详情](docs/coverage/unixbench_results.md)

---

## 二、openruyi-autotest 用户指南

参见 [用户指南](docs/user_guide_zh.md) — 涵盖从克隆仓库、安装依赖到执行单个用例、测试套、测试类型全量用例以及全部测试的完整步骤。

---

## 三、openruyi-autotest 开发指南

参见 [开发指南](docs/development-guide_zh.md) — 涵盖如何添加新测试用例、目录约定、BeakerLib 生命周期、FMF 元数据规范以及命名规范。

---

## 四、openruyi-autotest 测试报告模版

参见 [测试报告模版](docs/test_reports_zh.md) — 涵盖测试概述、各类型测试的套数/用例数/通过/失败/跳过统计表格。

---

## 五、许可证

openruyi-autotest 采用 [木兰宽松许可证，第2版（Mulan PSL v2）](LICENSE)。

CopyrightText (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
CopyrightText (C) 2026 openRuyi Project Contributors
