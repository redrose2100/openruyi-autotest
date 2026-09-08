# 功能测试覆盖详情

> 最后更新: 2026-06-16 | 自动生成
> 测试环境: openRuyi (10.20.237.192)

共 **202** 个软件包，**561** 个测试用例，**1692** 个功能点

## 全部软件包一览

| 软件包 | 用例数 | 功能点 | 类型 |
|--------|:---:|:---:|:---:|
| [acl](#acl) | 10 | 81 | rlRun |
| [atf](#atf) | 2 | 3 | rlRun |
| [attr](#attr) | 1 | 6 | rlRun |
| [audit](#audit) | 2 | 15 | rlRun |
| [authselect](#authselect) | 1 | 1 | rlRun |
| [autoconf](#autoconf) | 1 | 4 | rlRun |
| [automake](#automake) | 1 | 4 | rlRun |
| [bash](#bash) | 7 | 7 | rlRun |
| [bash-completion](#bashcompletion) | 1 | 1 | rlRun |
| [bc](#bc) | 1 | 2 | rlRun |
| [beakerlib](#beakerlib) | 1 | 1 | 简单 |
| [binutils](#binutils) | 1 | 1 | 简单 |
| [bison](#bison) | 2 | 3 | rlRun |
| [boost](#boost) | 1 | 4 | rlRun |
| [brotli](#brotli) | 1 | 1 | rlRun |
| [bzip2](#bzip2) | 1 | 1 | rlRun |
| [ca-certificates](#cacertificates) | 2 | 3 | rlRun |
| [ca-certificates-mozilla](#cacertificatesmozilla) | 1 | 2 | rlRun |
| [chkconfig](#chkconfig) | 1 | 1 | rlRun |
| [chrpath](#chrpath) | 2 | 3 | rlRun |
| [clang](#clang) | 15 | 25 | rlRun |
| [cloud-utils-growpart](#cloudutilsgrowpart) | 6 | 10 | rlRun |
| [cmake](#cmake) | 6 | 6 | 分段 |
| [cmocka](#cmocka) | 1 | 4 | rlRun |
| [config](#config) | 2 | 3 | rlRun |
| [coreutils](#coreutils) | 24 | 234 | rlRun |
| [cpio](#cpio) | 1 | 1 | rlRun |
| [cracklib](#cracklib) | 1 | 1 | 简单 |
| [cryptsetup](#cryptsetup) | 2 | 3 | rlRun |
| [curl](#curl) | 6 | 11 | rlRun |
| [dbus](#dbus) | 1 | 1 | rlRun |
| [dbus-broker](#dbusbroker) | 1 | 1 | rlRun |
| [debugedit](#debugedit) | 2 | 5 | rlRun |
| [dejagnu](#dejagnu) | 2 | 3 | rlRun |
| [diffutils](#diffutils) | 1 | 4 | rlRun |
| [dnf5-plugins](#dnf5plugins) | 10 | 11 | rlRun |
| [dos2unix](#dos2unix) | 2 | 3 | rlRun |
| [dwz](#dwz) | 2 | 3 | rlRun |
| [e2fsprogs](#e2fsprogs) | 1 | 1 | 简单 |
| [ed](#ed) | 2 | 3 | rlRun |
| [elfutils](#elfutils) | 2 | 31 | rlRun |
| [expat](#expat) | 1 | 1 | rlRun |
| [expect](#expect) | 2 | 3 | rlRun |
| [fdupes](#fdupes) | 2 | 3 | rlRun |
| [file](#file) | 1 | 1 | rlRun |
| [filesystem](#filesystem) | 1 | 2 | rlRun |
| [findutils](#findutils) | 5 | 13 | rlRun |
| [flex](#flex) | 2 | 3 | rlRun |
| [gawk](#gawk) | 1 | 2 | rlRun |
| [gcc](#gcc) | 12 | 52 | rlRun |
| [gcc16](#gcc16) | 1 | 1 | 简单 |
| [gdb](#gdb) | 2 | 3 | rlRun |
| [gdbm](#gdbm) | 2 | 3 | rlRun |
| [git](#git) | 1 | 1 | rlRun |
| [glib](#glib) | 1 | 1 | 简单 |
| [glibc](#glibc) | 2 | 17 | rlRun |
| [gmp](#gmp) | 1 | 2 | rlRun |
| [gnutls](#gnutls) | 1 | 1 | 简单 |
| [gobject-introspection](#gobjectintrospection) | 2 | 3 | rlRun |
| [gpm](#gpm) | 1 | 5 | rlRun |
| [grep](#grep) | 13 | 44 | rlRun |
| [groff](#groff) | 2 | 3 | rlRun |
| [gzip](#gzip) | 2 | 29 | rlRun |
| [help2man](#help2man) | 2 | 3 | rlRun |
| [icu4c](#icu4c) | 1 | 1 | 简单 |
| [iproute2](#iproute2) | 1 | 1 | 简单 |
| [iptables](#iptables) | 2 | 3 | rlRun |
| [iputils](#iputils) | 10 | 33 | 分段 |
| [isl](#isl) | 1 | 2 | rlRun |
| [iso-codes](#isocodes) | 1 | 1 | rlRun |
| [jitterentropy](#jitterentropy) | 1 | 2 | rlRun |
| [json-c](#jsonc) | 1 | 2 | rlRun |
| [kbd](#kbd) | 1 | 1 | 简单 |
| [keyutils](#keyutils) | 1 | 1 | 简单 |
| [kmod](#kmod) | 1 | 1 | 简单 |
| [krb5](#krb5) | 1 | 1 | 简单 |
| [kyua](#kyua) | 2 | 3 | rlRun |
| [labwc](#labwc) | 9 | 10 | rlRun |
| [less](#less) | 1 | 3 | rlRun |
| [libaio](#libaio) | 1 | 2 | rlRun |
| [libarchive](#libarchive) | 1 | 2 | rlRun |
| [libbpf](#libbpf) | 1 | 2 | rlRun |
| [libcap](#libcap) | 1 | 2 | rlRun |
| [libcap-ng](#libcapng) | 1 | 2 | rlRun |
| [libeconf](#libeconf) | 1 | 2 | rlRun |
| [libedit](#libedit) | 1 | 2 | rlRun |
| [libevent](#libevent) | 1 | 2 | rlRun |
| [libffi](#libffi) | 1 | 2 | rlRun |
| [libgcrypt](#libgcrypt) | 1 | 2 | rlRun |
| [libgpg-error](#libgpgerror) | 1 | 2 | rlRun |
| [libidn2](#libidn2) | 1 | 1 | rlRun |
| [libmicrohttpd](#libmicrohttpd) | 1 | 4 | rlRun |
| [libmnl](#libmnl) | 1 | 2 | rlRun |
| [libnetfilter_conntrack](#libnetfilter_conntrack) | 1 | 2 | rlRun |
| [libnfnetlink](#libnfnetlink) | 1 | 2 | rlRun |
| [libnftnl](#libnftnl) | 1 | 2 | rlRun |
| [libnl](#libnl) | 1 | 2 | rlRun |
| [libpcap](#libpcap) | 1 | 4 | rlRun |
| [libpng](#libpng) | 1 | 1 | rlRun |
| [libpsl](#libpsl) | 1 | 2 | rlRun |
| [libpwquality](#libpwquality) | 1 | 2 | rlRun |
| [libseccomp](#libseccomp) | 1 | 2 | rlRun |
| [libselinux](#libselinux) | 1 | 2 | rlRun |
| [libsepol](#libsepol) | 1 | 2 | rlRun |
| [libsodium](#libsodium) | 1 | 4 | rlRun |
| [libssh](#libssh) | 1 | 4 | rlRun |
| [libtasn1](#libtasn1) | 1 | 3 | rlRun |
| [libtirpc](#libtirpc) | 1 | 2 | rlRun |
| [libtool](#libtool) | 2 | 3 | rlRun |
| [libunistring](#libunistring) | 1 | 2 | rlRun |
| [libxcrypt](#libxcrypt) | 1 | 2 | rlRun |
| [libxml2](#libxml2) | 1 | 2 | rlRun |
| [libxslt](#libxslt) | 1 | 1 | rlRun |
| [linux-headers](#linuxheaders) | 1 | 2 | rlRun |
| [lua](#lua) | 2 | 5 | rlRun |
| [lutok](#lutok) | 1 | 4 | rlRun |
| [lvm2](#lvm2) | 1 | 1 | 简单 |
| [lz4](#lz4) | 1 | 4 | rlRun |
| [lzip](#lzip) | 2 | 3 | rlRun |
| [make](#make) | 9 | 21 | rlRun |
| [meson](#meson) | 1 | 4 | rlRun |
| [mpc](#mpc) | 1 | 2 | rlRun |
| [mpdecimal](#mpdecimal) | 1 | 2 | rlRun |
| [mpfr](#mpfr) | 1 | 2 | rlRun |
| [ncurses](#ncurses) | 1 | 1 | 简单 |
| [nettle](#nettle) | 2 | 11 | rlRun |
| [newt](#newt) | 2 | 3 | rlRun |
| [nfs-utils](#nfsutils) | 1 | 5 | rlRun |
| [nghttp2](#nghttp2) | 1 | 2 | rlRun |
| [ninja](#ninja) | 1 | 4 | rlRun |
| [nss](#nss) | 2 | 3 | rlRun |
| [nss_wrapper](#nss_wrapper) | 1 | 4 | rlRun |
| [openruyi-release](#openruyirelease) | 1 | 1 | rlRun |
| [openssh](#openssh) | 1 | 1 | rlRun |
| [openssh-clients](#opensshclients) | 7 | 19 | rlRun |
| [openssl](#openssl) | 1 | 1 | rlRun |
| [p11-kit](#p11kit) | 1 | 1 | 简单 |
| [pam](#pam) | 2 | 11 | rlRun |
| [patch](#patch) | 1 | 1 | rlRun |
| [pciutils](#pciutils) | 13 | 13 | 分段 |
| [pcre2](#pcre2) | 1 | 2 | rlRun |
| [perl](#perl) | 1 | 1 | rlRun |
| [perl-Error](#perlError) | 1 | 4 | rlRun |
| [perl-Locale-gettext](#perlLocalegettext) | 1 | 4 | rlRun |
| [perl-rpm-packaging](#perlrpmpackaging) | 1 | 4 | rlRun |
| [pkgconf](#pkgconf) | 2 | 5 | rlRun |
| [podman](#podman) | 7 | 16 | rlRun |
| [podmansh](#podmansh) | 11 | 11 | 分段 |
| [popt](#popt) | 1 | 2 | rlRun |
| [procps-ng](#procpsng) | 14 | 53 | 分段 |
| [psmisc](#psmisc) | 13 | 22 | 分段 |
| [publicsuffix-list](#publicsuffixlist) | 1 | 1 | rlRun |
| [pyproject-rpm-macros](#pyprojectrpmmacros) | 1 | 1 | rlRun |
| [python](#python) | 5 | 8 | rlRun |
| [python-flit-core](#pythonflitcore) | 1 | 4 | rlRun |
| [python-lxml](#pythonlxml) | 1 | 2 | rlRun |
| [python-packaging](#pythonpackaging) | 1 | 1 | rlRun |
| [python-pip](#pythonpip) | 1 | 1 | rlRun |
| [python-pyelftools](#pythonpyelftools) | 1 | 4 | rlRun |
| [python-rpm-generators](#pythonrpmgenerators) | 1 | 4 | rlRun |
| [python-rpm-macros](#pythonrpmmacros) | 1 | 1 | rlRun |
| [python-setuptools](#pythonsetuptools) | 1 | 4 | rlRun |
| [python-srpm-macros](#pythonsrpmmacros) | 1 | 1 | rlRun |
| [python-wheel](#pythonwheel) | 1 | 4 | rlRun |
| [re2c](#re2c) | 2 | 3 | rlRun |
| [readline](#readline) | 1 | 2 | rlRun |
| [rpm](#rpm) | 1 | 1 | rlRun |
| [rpm-config-openruyi](#rpmconfigopenruyi) | 1 | 2 | rlRun |
| [rpmbuild](#rpmbuild) | 9 | 20 | 分段 |
| [rsync](#rsync) | 2 | 3 | rlRun |
| [scdoc](#scdoc) | 2 | 3 | rlRun |
| [sddm](#sddm) | 5 | 10 | rlRun |
| [sed](#sed) | 6 | 12 | rlRun |
| [setup](#setup) | 1 | 1 | rlRun |
| [slang](#slang) | 1 | 1 | rlRun |
| [socket_wrapper](#socket_wrapper) | 1 | 4 | rlRun |
| [source-highlight](#sourcehighlight) | 2 | 3 | rlRun |
| [sqlite](#sqlite) | 1 | 2 | rlRun |
| [swig](#swig) | 2 | 3 | rlRun |
| [systemd](#systemd) | 36 | 114 | rlRun |
| [systemd-timesyncd](#systemdtimesyncd) | 5 | 13 | rlRun |
| [systemtap](#systemtap) | 2 | 3 | rlRun |
| [tar](#tar) | 10 | 27 | 分段 |
| [tcl](#tcl) | 2 | 3 | rlRun |
| [tcsh](#tcsh) | 1 | 1 | rlRun |
| [texinfo](#texinfo) | 2 | 3 | rlRun |
| [time](#time) | 1 | 1 | rlRun |
| [tmux](#tmux) | 22 | 179 | rlRun |
| [tzdata](#tzdata) | 1 | 3 | rlRun |
| [uid_wrapper](#uid_wrapper) | 1 | 4 | rlRun |
| [unbound](#unbound) | 1 | 5 | rlRun |
| [unzip](#unzip) | 1 | 4 | rlRun |
| [util-linux](#utillinux) | 2 | 31 | rlRun |
| [vim](#vim) | 1 | 1 | rlRun |
| [weston](#weston) | 9 | 9 | rlRun |
| [wget](#wget) | 15 | 18 | 分段 |
| [wget2](#wget2) | 15 | 17 | 分段 |
| [which](#which) | 1 | 1 | rlRun |
| [xmlto](#xmlto) | 2 | 3 | rlRun |
| [xxhash](#xxhash) | 2 | 3 | rlRun |
| [xz](#xz) | 2 | 31 | rlRun |
| [zstd](#zstd) | 2 | 13 | rlRun |

---

## acl

<details>
<summary><b>acl — 10 个用例 / 81 个功能点</b></summary>

#### test_acl_getfacl_basic

- 查看文件默认 ACL
- 查看目录默认 ACL
- 使用 -a 参数查看 access ACL
- 使用 -d 参数查看 default ACL
- 使用 -c 参数不显示注释头
- 使用 -n 参数显示数字 ID
- 使用 -t 参数表格输出

#### test_acl_setfacl_basic

- 设置用户 root 的 rwx 权限
- 验证 ACL 设置
- 设置组 root 的 r-x 权限
- 验证 ACL 设置
- 设置 other 的只读权限
- 验证 ACL 设置
- 设置 mask 为 rwx
- 验证 mask 设置
- 使用 -n 参数不重新计算 mask
- 验证 ACL 设置

#### test_acl_setfacl_advanced

- 为目录设置 default user ACL
- 验证 default ACL 设置
- 为目录设置 default group ACL
- 验证 default group ACL
- 为目录设置 default mask
- 验证 default mask
- 为目录设置 default other
- 验证 default other
- 使用 --set 替换整个 ACL
- 验证 ACL 替换
- 创建 ACL 规则文件
- 从文件读取并应用 ACL
- 验证从文件应用的 ACL

#### test_acl_setfacl_remove

- 删除用户 root 的 ACL 条目
- 验证 ACL 删除
- 删除组 root 的 ACL 条目
- 验证 ACL 删除
- 删除所有扩展 ACL
- 验证所有扩展 ACL 已删除
- 删除目录的 default ACL
- 验证 default ACL 已删除
- 创建删除规则文件
- 先添加用户 ACL
- 从文件读取并删除 ACL
- 验证从文件删除的 ACL

#### test_acl_setfacl_recursive

- 创建多层子目录
- 创建测试文件
- 递归设置 user ACL
- 验证递归设置 - file1
- 验证递归设置 - file2
- 递归删除所有扩展 ACL
- 验证递归删除 - file1
- 验证递归删除 - file2

#### test_acl_setfacl_symlink

- 创建符号链接
- 使用 -L 跟随符号链接设置 ACL
- 验证符号链接目标文件的 ACL
- 使用 -P 不跟随符号链接

#### test_acl_chacl

- 先清理 ACL
- 使用 chacl 查看 ACL
- 使用 chacl 设置基本 ACL
- 验证 chacl 设置的 ACL
- 使用 chacl 设置 default ACL
- 验证 chacl 设置的 default ACL
- 使用 chacl 递归设置 ACL
- 验证 chacl 递归设置
- 使用 chacl -b 同时设置
- 验证 chacl -b 设置

#### test_acl_inheritance

- 设置目录 default ACL
- 在目录中创建新文件
- 验证新文件继承了 default ACL
- 在目录中创建子目录
- 验证子目录继承了 default ACL

#### test_acl_permission_verify

- 设置完整权限
- 验证权限设置
- 设置 mask 限制有效权限
- 验证 mask 限制后的有效权限

#### test_acl_special_cases

- 设置多个用户和组 ACL
- 验证多个 ACL 条目
- 设置测试 ACL
- 导出 ACL 备份
- 清除 ACL
- 尝试恢复 ACL
- 使用 --test 模式不实际修改
- 验证 --test 模式未修改 ACL

</details>

---

## atf

<details>
<summary><b>atf — 2 个用例 / 3 个功能点</b></summary>

#### test_atf_atf_basic

- 检查主要工具可执行性

#### test_atf_atf_version

- 获取 atf 帮助信息
- 获取 atf 版本信息

</details>

---

## attr

<details>
<summary><b>attr — 1 个用例 / 6 个功能点</b></summary>

#### test_attr_main

- 获取 attr 版本信息
- 获取 getfattr 版本信息
- 获取 setfattr 版本信息
- 切换目录
- 创建文件
- 创建目录

</details>

---

## audit

<details>
<summary><b>audit — 2 个用例 / 15 个功能点</b></summary>

#### test_audit_version_help

- auditctl 版本信息
- auditctl 帮助信息
- ausearch 版本信息
- ausearch 帮助信息
- aureport 版本信息
- aureport 帮助信息
- aulast 版本信息
- aulast 帮助信息
- aulastlog 版本信息
- aulastlog 帮助信息
- ausyscall 版本信息
- ausyscall 帮助信息
- augenrules 版本信息
- augenrules 帮助信息

#### test_audit_error_handling

- auditctl: 无效选项

</details>

---

## authselect

<details>
<summary><b>authselect — 1 个用例 / 1 个功能点</b></summary>

#### test_authselect_main

- 获取 authselect 版本信息

</details>

---

## autoconf

<details>
<summary><b>autoconf — 1 个用例 / 4 个功能点</b></summary>

#### test_autoconf_main

- 获取 autoconf 版本信息
- 列出包内二进制文件
- 获取 autoconf 版本输出
- 检查手册页

</details>

---

## automake

<details>
<summary><b>automake — 1 个用例 / 4 个功能点</b></summary>

#### test_automake_main

- 获取 automake 版本信息
- 列出包内二进制文件
- 获取 automake 版本输出
- 检查手册页

</details>

---

## bash

<details>
<summary><b>bash — 7 个用例 / 7 个功能点</b></summary>

#### test_bash_basic_script

- bash 执行脚本

#### test_bash_variables_loops

- bash -c: for循环

#### test_bash_conditionals

- bash: if条件

#### test_bash_functions

- bash: 函数定义调用

#### test_bash_pipe_redirect

- bash: 管道

#### test_bash_bashbug

- bashbug 帮助

#### test_bash_error_handling

- bash: 错误退出

</details>

---

## bash-completion

<details>
<summary><b>bash-completion — 1 个用例 / 1 个功能点</b></summary>

#### test_bash_completion_main

- 检查包已安装

</details>

---

## bc

<details>
<summary><b>bc — 1 个用例 / 2 个功能点</b></summary>

#### test_bc_main

- 获取 bc 版本信息
- 获取 dc 版本信息

</details>

---

## beakerlib

<details>
<summary><b>beakerlib — 1 个用例 / 1 个功能点</b></summary>

#### test_beakerlib_basic_check

- 检查 beakerlib 已安装

</details>

---

## binutils

<details>
<summary><b>binutils — 1 个用例 / 1 个功能点</b></summary>

#### test_binutils_basic_check

- 检查 binutils 已安装

</details>

---

## bison

<details>
<summary><b>bison — 2 个用例 / 3 个功能点</b></summary>

#### test_bison_bison_basic

- 检查主要工具可执行性

#### test_bison_bison_version

- 获取 bison 帮助信息
- 获取 bison 版本信息

</details>

---

## boost

<details>
<summary><b>boost — 1 个用例 / 4 个功能点</b></summary>

#### test_boost_main

- 获取 boost 版本信息
- 列出 boost 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## brotli

<details>
<summary><b>brotli — 1 个用例 / 1 个功能点</b></summary>

#### test_brotli_main

- 获取 brotli 版本信息

</details>

---

## bzip2

<details>
<summary><b>bzip2 — 1 个用例 / 1 个功能点</b></summary>

#### test_bzip2_main

- 获取 bzip2 版本信息

</details>

---

## ca-certificates

<details>
<summary><b>ca-certificates — 2 个用例 / 3 个功能点</b></summary>

#### test_ca_certificates_version_help

- update-ca-trust 版本信息
- update-ca-trust 帮助信息

#### test_ca_certificates_error_handling

- update-ca-trust: 无效选项

</details>

---

## ca-certificates-mozilla

<details>
<summary><b>ca-certificates-mozilla — 1 个用例 / 2 个功能点</b></summary>

#### test_ca_certificates_mozilla_version_help

- 列出包文件
- 库文件检查

</details>

---

## chkconfig

<details>
<summary><b>chkconfig — 1 个用例 / 1 个功能点</b></summary>

#### test_chkconfig_main

- 获取 chkconfig 版本信息

</details>

---

## chrpath

<details>
<summary><b>chrpath — 2 个用例 / 3 个功能点</b></summary>

#### test_chrpath_chrpath_basic

- 检查主要工具可执行性

#### test_chrpath_chrpath_version

- 获取 chrpath 帮助信息
- 获取 chrpath 版本信息

</details>

---

## clang

<details>
<summary><b>clang — 15 个用例 / 25 个功能点</b></summary>

#### test_clang_basic_c_compilation

- Compile hello.c
- Run compiled binary
- Output is ELF binary

#### test_clang_basic_c_compilation

- Compile C++ from hello.c
- Run C++ binary

#### test_clang_compileonly

- clang -c: compile only
- Object file exists

#### test_clang_optimization_levels

- Optimization -$lvl

#### test_clang_debug_and_warnings

- Debug symbols
- -Wall warnings
- -Wextra warnings
- -Werror

#### test_clang_c_standards

- C standard: $std

#### test_clang_c_standards

- C++ standard: $std

#### test_clang_preprocessor

- clang -E: preprocess
- clang -dM: dump macros

#### test_clang_static_analysis

- clang --analyze: static analysis

#### test_clang_clangcl_msvc_compat

- clang-cl help

#### test_clang_clangcpp

- clang-cpp: preprocessor

#### test_clang_clangscandeps

- clang-scan-deps help

#### test_clang_linking_options

- Compile with -fPIC
- clang -shared: shared library

#### test_clang_verbose_mode

- clang -v: verbose

#### test_clang_error_handling

- Compilation error
- Invalid option

</details>

---

## cloud-utils-growpart

<details>
<summary><b>cloud-utils-growpart — 6 个用例 / 10 个功能点</b></summary>

#### test_cloud_utils_growpart_help_and_version

- growpart help
- growpart -h: short help

#### test_cloud_utils_growpart_diskpartition_info

- lsblk: list block devices
- df: disk free space

#### test_cloud_utils_growpart_dryrun_no_actual_resize

- growpart -N: dry run

#### test_cloud_utils_growpart_free_percent_option

- growpart: has free-percent option

#### test_cloud_utils_growpart_fudge_factor_option

- growpart: has fudge option

#### test_cloud_utils_growpart_error_handling

- growpart: no args (expected fail)
- growpart: nonexistent disk
- growpart: invalid option

</details>

---

## cmake

<details>
<summary><b>cmake — 6 个用例 / 6 个功能点</b></summary>

#### test_cmake_basic_cmake_project

- include <stdio.h>

#### test_cmake_cmake_configure

- test_cmake_cmake_configure

#### test_cmake_cmake_e_mode

- test_cmake_cmake_e_mode

#### test_cmake_ctest_and_cpack

- test_cmake_ctest_and_cpack

#### test_cmake_error_handling

- test_cmake_error_handling

#### test_cmake_cmake_version_and_help

- test_cmake_cmake_version_and_help

</details>

---

## cmocka

<details>
<summary><b>cmocka — 1 个用例 / 4 个功能点</b></summary>

#### test_cmocka_main

- 获取 cmocka 版本信息
- 列出 cmocka 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## config

<details>
<summary><b>config — 2 个用例 / 3 个功能点</b></summary>

#### test_config_config

- 检查主要工具可执行性

#### test_config_config

- 获取 config 帮助信息
- 获取 config 版本信息

</details>

---

## coreutils

<details>
<summary><b>coreutils — 24 个用例 / 234 个功能点</b></summary>

#### test_coreutils_file_creation_and_listing_echo_cat_ls_dir_vdir

- echo create file
- echo append
- echo -n suppress newline
- echo -n: verify no trailing newline
- cat display file
- cat: verify 2 lines
- cat -n number all lines
- cat -b number non-blank lines
- ls -la list all files
- ls specific file
- ls -l: regular file check
- ls -ld: directory check
- ls -1 single column
- dir list directory
- vdir long format list

#### test_coreutils_copy_move_remove_cp_mv_rm_rmdir

- cp copy file
- cp: verify copy exists
- cp: files identical
- cp -r recursive copy
- cp -r: verify directory copy
- mv rename file
- mv: old name gone
- mv: new name exists
- mv to subdirectory
- Create temp file
- rm remove file
- rm: file removed
- Create dir to remove
- rm -rf recursive force
- rm -rf: directory removed
- Create empty directory
- rmdir remove empty directory
- rmdir: directory removed

#### test_coreutils_directory_file_creation_temp_files_mkdir_touch_mktemp

- mkdir -p nested directories
- mkdir -p: verify nested dir
- mkdir -m set mode
- touch create file
- touch: file exists
- touch -t set timestamp
- touch -a access time only

#### test_coreutils_links_and_path_resolution_ln_link_unlink_readlink_realpath

- Create link source
- ln create hard link
- ln: hard link same inode
- ln -s symbolic link
- ln -s: symlink exists
- ln -s: read through symlink
- ln -sf force recreate symlink
- link create hard link
- link: same inode
- unlink remove hard link
- unlink: file removed
- readlink show symlink target
- readlink: correct target
- readlink -f canonicalize
- realpath canonical path

#### test_coreutils_file_viewing_head_tail_tac_nl

- head -n 5: first 5 lines
- head -n 3: verify count
- head -c 10: first 10 bytes
- tail -n 5: last 5 lines
- tail -n 3: verify count
- tail -n +18: from line 18
- tail -c 10: last 10 bytes
- tac reverse lines
- tac: first becomes last
- nl number lines

#### test_coreutils_counting_and_statistics_wc_du_df_stat

- wc -l line count
- wc -l: 20 lines
- wc -c byte count
- wc -w word count
- wc -m character count
- du -sh summary human
- du -h directory usage
- df -h human readable
- df: root filesystem
- stat file status
- stat -c format output
- stat -f filesystem status

#### test_coreutils_text_processing_i_sort_uniq_cut_tr

- sort alphabetically
- sort: first is apple
- sort -r reverse
- sort -u unique
- sort -n numeric
- uniq unique lines
- uniq: 4 unique
- uniq -c count occurrences
- uniq -d only duplicates
- uniq -u only uniques
- cut -d: -f1 first field
- cut -d: -f2 second field
- cut multiple fields
- cut -c character range
- tr translate uppercase to lowercase
- tr -d delete characters
- tr -s squeeze repeats

#### test_coreutils_text_processing_ii_paste_comm_join_fmt_fold_pr_expand_unexpand

- paste merge files side by side
- paste -d: custom delimiter
- paste -s serial
- comm compare sorted files
- join files on common field
- fmt reformat text
- fmt -w set width
- fold -w wrap at width
- pr paginate file
- pr -n number lines
- expand tabs to spaces
- unexpand -a spaces to tabs

#### test_coreutils_octal_dump_od

- od octal dump
- od -c character dump
- od -x hex dump
- od -A x hex address

#### test_coreutils_path_operations_basename_dirname_pwd

- basename extract filename
- basename strip suffix
- dirname extract directory
- dirname path extraction
- pwd print working directory

#### test_coreutils_permissions_and_ownership_chmod_chown_chgrp

- Create permission test file
- chmod u+x add exec
- chmod: verify exec set
- chmod 644 numeric
- chmod: verify 644 perms
- Setup recursive chmod
- chmod -R recursive
- chown version check
- chown to self
- chgrp version check

#### test_coreutils_redirection_tee

- tee write to file
- tee: verify output
- tee -a append mode

#### test_coreutils_checksums_cksum_md5sum_sha1sum_sha224sum_sha384sum_sha512sum_sha256sum_b2sum_sum

- cksum CRC checksum
- md5sum compute
- md5sum save
- md5sum -c verify
- sha1sum compute
- sha1sum save
- sha1sum -c verify
- sha224sum compute
- sha256sum compute
- sha256sum save
- sha256sum -c verify
- sha384sum compute
- sha512sum compute
- b2sum BLAKE2 checksum
- sum BSD checksum

#### test_coreutils_encoding_base32_base64_basenc

- base32 encode
- base32 -d decode
- base64 encode
- base64 -d decode
- basenc --base64 encode

#### test_coreutils_system_information_uname_who_whoami_id_groups_users_hostid_nproc_tty_logname_pinky

- uname system name
- uname -a all info
- uname -r kernel release
- uname -m machine hardware
- who show logged in users
- whoami current user
- id user identity
- id -u user ID
- id -g group ID
- groups show group membership
- groups for specific user
- users list logged in users
- hostid numeric host identifier
- nproc number of CPUs
- nproc --all all processors
- tty terminal name
- logname login name
- pinky user info

#### test_coreutils_boolean_and_condition_true_false_test

- true returns success
- false returns failure
- test -f: file exists
- test -d: directory exists
- test string equality
- test numeric comparison
- [ -f: file exists
- [ string equality

#### test_coreutils_environment_and_time_env_printenv_date_printf

- env show environment
- env set variable for command
- printenv show PATH
- date current date/time
- date custom format
- date -u UTC time
- printf formatted output
- printf string output

#### test_coreutils_flow_control_sleep_timeout_yes

- sleep delay
- timeout: command finishes in time
- timeout: successful completion
- timeout: kills slow command
- yes repeated output
- yes custom string

#### test_coreutils_process_control_nice_nohup_stdbuf

- nice adjust priority
- nohup run command
- stdbuf line buffered output

#### test_coreutils_file_operations_dd_truncate_shred_sync_install_chroot

- dd copy file
- truncate set size
- truncate: verify size
- Create file to shred
- shred remove file securely
- shred: file removed
- sync flush filesystem buffers
- install copy with mode
- install: destination exists
- install -d create directory
- install -d: directory exists
- chroot version check
- mkfifo create named pipe
- mkfifo: verify pipe created
- mknod version check

#### test_coreutils_numbers_and_expressions_seq_factor_shuf_numfmt_expr

- seq generate sequence
- seq: 5 numbers
- seq -s custom separator
- factor prime factorization
- factor prime number
- shuf randomize lines
- shuf: same line count
- numfmt to SI units
- numfmt from SI units
- numfmt to IEC units
- expr basic arithmetic
- expr multiplication
- expr string length

#### test_coreutils_split_files_split_csplit

- split by lines
- split: multiple output files
- csplit split by pattern

#### test_coreutils_special_utilities_stty_pathchk_tsort_ptx_dircolors

- stty -a show all terminal settings
- pathchk validate path
- pathchk -p POSIX check
- tsort topological sort
- ptx permuted index
- dircolors -p print database
- dircolors output LS_COLORS

#### test_coreutils_error_handling

- cp: error on nonexistent source
- ls: error on nonexistent file
- mkdir: error on existing dir
- rm: error on dir without -r
- rmdir: error on non-empty dir

</details>

---

## cpio

<details>
<summary><b>cpio — 1 个用例 / 1 个功能点</b></summary>

#### test_cpio_main

- 获取 cpio 版本信息

</details>

---

## cracklib

<details>
<summary><b>cracklib — 1 个用例 / 1 个功能点</b></summary>

#### test_cracklib_basic_check

- 检查 cracklib 已安装

</details>

---

## cryptsetup

<details>
<summary><b>cryptsetup — 2 个用例 / 3 个功能点</b></summary>

#### test_cryptsetup_version_help

- cryptsetup 版本信息
- cryptsetup 帮助信息

#### test_cryptsetup_error_handling

- cryptsetup: 无效选项

</details>

---

## curl

<details>
<summary><b>curl — 6 个用例 / 11 个功能点</b></summary>

#### test_curl_basic_download

- curl 下载示例页面
- curl -I: 仅获取响应头

#### test_curl_output_options

- curl -o: 输出到文件
- curl -O: 远程文件名

#### test_curl_verbose_mode

- curl -v: 详细模式
- curl -s: 静默模式

#### test_curl_basic

- curl -L: 跟随重定向
- curl -k: 忽略SSL证书
- curl --connect-timeout: 连接超时

#### test_curl_wcurl

- wcurl 帮助

#### test_curl_error_handling

- curl: 无效选项

</details>

---

## dbus

<details>
<summary><b>dbus — 1 个用例 / 1 个功能点</b></summary>

#### test_dbus_main

- 获取 dbus-launch 版本信息

</details>

---

## dbus-broker

<details>
<summary><b>dbus-broker — 1 个用例 / 1 个功能点</b></summary>

#### test_dbus_broker_main

- 获取 dbus-broker 版本信息

</details>

---

## debugedit

<details>
<summary><b>debugedit — 2 个用例 / 5 个功能点</b></summary>

#### test_debugedit_version_help

- debugedit 版本信息
- debugedit 帮助信息
- debugedit-classify-ar 版本信息
- debugedit-classify-ar 帮助信息

#### test_debugedit_error_handling

- debugedit: 无效选项

</details>

---

## dejagnu

<details>
<summary><b>dejagnu — 2 个用例 / 3 个功能点</b></summary>

#### test_dejagnu_dejagnu_basic

- 检查主要工具可执行性

#### test_dejagnu_dejagnu_version

- 获取 dejagnu 帮助信息
- 获取 dejagnu 版本信息

</details>

---

## diffutils

<details>
<summary><b>diffutils — 1 个用例 / 4 个功能点</b></summary>

#### test_diffutils_main

- 获取 cmp 版本信息
- 获取 diff 版本信息
- 获取 diff3 版本信息
- 获取 sdiff 版本信息

</details>

---

## dnf5-plugins

<details>
<summary><b>dnf5-plugins — 10 个用例 / 11 个功能点</b></summary>

#### test_dnf5_plugins_dnf5_version

- dnf5 version

#### test_dnf5_plugins_dnf5_help

- dnf5 help

#### test_dnf5_plugins_list_installed_plugins

- Plugin files
- Plugin directory

#### test_dnf5_plugins_available_plugins

- Check plugin: $plugin

#### test_dnf5_plugins_commands_with_plugins

- Plugin commands in help

#### test_dnf5_plugins_dnf5_repoquery

- dnf5 repoquery help

#### test_dnf5_plugins_dnf5_repolist

- dnf5 repolist

#### test_dnf5_plugins_dnf5_list

- dnf5 list installed

#### test_dnf5_plugins_dnf5_info

- dnf5 info

#### test_dnf5_plugins_error_handling

- dnf5: invalid option

</details>

---

## dos2unix

<details>
<summary><b>dos2unix — 2 个用例 / 3 个功能点</b></summary>

#### test_dos2unix_dos2unix_basic

- 检查主要工具可执行性

#### test_dos2unix_dos2unix_version

- 获取 dos2unix 帮助信息
- 获取 dos2unix 版本信息

</details>

---

## dwz

<details>
<summary><b>dwz — 2 个用例 / 3 个功能点</b></summary>

#### test_dwz_version_help

- dwz 版本信息
- dwz 帮助信息

#### test_dwz_error_handling

- dwz: 无效选项

</details>

---

## e2fsprogs

<details>
<summary><b>e2fsprogs — 1 个用例 / 1 个功能点</b></summary>

#### test_e2fsprogs_basic_check

- 检查 e2fsprogs 已安装

</details>

---

## ed

<details>
<summary><b>ed — 2 个用例 / 3 个功能点</b></summary>

#### test_ed_ed_basic

- 检查主要工具可执行性

#### test_ed_ed_version

- 获取 ed 帮助信息
- 获取 ed 版本信息

</details>

---

## elfutils

<details>
<summary><b>elfutils — 2 个用例 / 31 个功能点</b></summary>

#### test_elfutils_version_help

- eu-addr2line 版本信息
- eu-addr2line 帮助信息
- eu-ar 版本信息
- eu-ar 帮助信息
- eu-elfclassify 版本信息
- eu-elfclassify 帮助信息
- eu-elfcmp 版本信息
- eu-elfcmp 帮助信息
- eu-elfcompress 版本信息
- eu-elfcompress 帮助信息
- eu-elflint 版本信息
- eu-elflint 帮助信息
- eu-findtextrel 版本信息
- eu-findtextrel 帮助信息
- eu-make-debug-archive 版本信息
- eu-make-debug-archive 帮助信息
- eu-nm 版本信息
- eu-nm 帮助信息
- eu-objdump 版本信息
- eu-objdump 帮助信息
- eu-ranlib 版本信息
- eu-ranlib 帮助信息
- eu-readelf 版本信息
- eu-readelf 帮助信息
- eu-size 版本信息
- eu-size 帮助信息
- eu-srcfiles 版本信息
- eu-srcfiles 帮助信息
- eu-stack 版本信息
- eu-stack 帮助信息

#### test_elfutils_error_handling

- eu-addr2line: 无效选项

</details>

---

## expat

<details>
<summary><b>expat — 1 个用例 / 1 个功能点</b></summary>

#### test_expat_main

- 获取 xmlwf 版本信息

</details>

---

## expect

<details>
<summary><b>expect — 2 个用例 / 3 个功能点</b></summary>

#### test_expect_expect_basic

- 检查主要工具可执行性

#### test_expect_expect_version

- 获取 expect 帮助信息
- 获取 expect 版本信息

</details>

---

## fdupes

<details>
<summary><b>fdupes — 2 个用例 / 3 个功能点</b></summary>

#### test_fdupes_fdupes_basic

- 检查主要工具可执行性

#### test_fdupes_fdupes_version

- 获取 fdupes 帮助信息
- 获取 fdupes 版本信息

</details>

---

## file

<details>
<summary><b>file — 1 个用例 / 1 个功能点</b></summary>

#### test_file_main

- 获取 file 版本信息

</details>

---

## filesystem

<details>
<summary><b>filesystem — 1 个用例 / 2 个功能点</b></summary>

#### test_filesystem_version_help

- 列出包文件
- 库文件检查

</details>

---

## findutils

<details>
<summary><b>findutils — 5 个用例 / 13 个功能点</b></summary>

#### test_findutils_find

- find -name: 按名称查找
- find -type f: 查找文件
- find -type d: 查找目录

#### test_findutils_find

- find -maxdepth: 最大深度
- find -mindepth: 最小深度
- find -empty: 空文件/目录
- find -size: 按大小

#### test_findutils_find

- find -exec: 执行命令
- find -delete: 删除文件
- find -delete: 验证删除

#### test_findutils_xargs

- xargs: 基本用法
- xargs -n1: 每次一个参数

#### test_findutils_error_handling

- find: 无效路径

</details>

---

## flex

<details>
<summary><b>flex — 2 个用例 / 3 个功能点</b></summary>

#### test_flex_flex_basic

- 检查主要工具可执行性

#### test_flex_flex_version

- 获取 flex 帮助信息
- 获取 flex 版本信息

</details>

---

## gawk

<details>
<summary><b>gawk — 1 个用例 / 2 个功能点</b></summary>

#### test_gawk_main

- 获取 awk 版本信息
- 获取 gawk 版本信息

</details>

---

## gcc

<details>
<summary><b>gcc — 12 个用例 / 52 个功能点</b></summary>

#### test_gcc_basic_c_compilation

- Compile hello.c to hello
- Run compiled hello
- Verify output is ELF binary
- Compile with -o flag
- Run myhello

#### test_gcc_c_compilation

- Compile hello.cpp
- Compile with C++11 standard

#### test_gcc_compiler_optimization_flags

- Compile with -O0
- Compile with -O2
- Compile with debug symbols -g
- Verify debug symbols present

#### test_gcc_preprocessor

- Preprocess with -E
- Verify macro expanded in preprocessed output
- Compile preprocessed .i file
- Run from preprocessed source
- Compile with -D flag
- Run with -D defined macro

#### test_gcc_assembly_output

- Generate assembly with -S
- Check main label in assembly
- Assemble to object file

#### test_gcc_linking_and_libraries

- Link with -lm
- Run math linked program
- Compile static binary

#### test_gcc_warning_flags

- Compile with -Wall warnings enabled
- Compile with -Werror
- Compile with -pedantic

#### test_gcc_multifile_compilation

- Compile add.c to object
- Compile main.c to object
- Link multiple objects
- Run multi-file program
- Compile multiple files in one command
- Run single-command multi-file program

#### test_gcc_code_coverage_gcov

- Compile with coverage flags
- Run coverage test program
- Run gcov
- Check gcov output file exists

#### test_gcc_error_handling

- Test type mismatch warning

#### test_gcc_special_features

- Compile with C99 standard
- Compile with __attribute__
- Run attribute test
- Compile with -I include path
- Run include path test

#### test_gcc_gcc_toolchain_utilities

- gcc-ar version check
- gcc-nm version check
- gcc-ranlib version check
- gcov-dump version check
- gcov-tool version check
- lto-dump version check
- cc version check
- cc equals gcc
- c++ version check
- c++ equals g++

</details>

---

## gcc16

<details>
<summary><b>gcc16 — 1 个用例 / 1 个功能点</b></summary>

#### test_gcc16_basic_check

- 检查 gcc16 已安装

</details>

---

## gdb

<details>
<summary><b>gdb — 2 个用例 / 3 个功能点</b></summary>

#### test_gdb_gdb_basic

- 检查主要工具可执行性

#### test_gdb_gdb_version

- 获取 gdb 帮助信息
- 获取 gdb 版本信息

</details>

---

## gdbm

<details>
<summary><b>gdbm — 2 个用例 / 3 个功能点</b></summary>

#### test_gdbm_gdbm

- 检查主要工具可执行性

#### test_gdbm_gdbm

- 获取 gdbm 帮助信息
- 获取 gdbm 版本信息

</details>

---

## git

<details>
<summary><b>git — 1 个用例 / 1 个功能点</b></summary>

#### test_git_main

- 检查包已安装

</details>

---

## glib

<details>
<summary><b>glib — 1 个用例 / 1 个功能点</b></summary>

#### test_glib_basic_check

- 检查 glib 已安装

</details>

---

## glibc

<details>
<summary><b>glibc — 2 个用例 / 17 个功能点</b></summary>

#### test_glibc_version_help

- gencat 版本信息
- gencat 帮助信息
- getconf 版本信息
- getconf 帮助信息
- getent 版本信息
- getent 帮助信息
- iconv 版本信息
- iconv 帮助信息
- ldconfig 版本信息
- ldconfig 帮助信息
- ldd 版本信息
- ldd 帮助信息
- locale 版本信息
- locale 帮助信息
- localedef 版本信息
- localedef 帮助信息

#### test_glibc_error_handling

- gencat: 无效选项

</details>

---

## gmp

<details>
<summary><b>gmp — 1 个用例 / 2 个功能点</b></summary>

#### test_gmp_version_help

- 列出包文件
- 库文件检查

</details>

---

## gnutls

<details>
<summary><b>gnutls — 1 个用例 / 1 个功能点</b></summary>

#### test_gnutls_basic_check

- 检查 gnutls 已安装

</details>

---

## gobject-introspection

<details>
<summary><b>gobject-introspection — 2 个用例 / 3 个功能点</b></summary>

#### test_gobject_introspection_gobject_introspection

- 检查主要工具可执行性

#### test_gobject_introspection_gobject_introspection

- 获取 gobject-introspection 帮助信息
- 获取 gobject-introspection 版本信息

</details>

---

## gpm

<details>
<summary><b>gpm — 1 个用例 / 5 个功能点</b></summary>

#### test_gpm_main

- 获取 gpm 版本信息
- 列出包内二进制文件
- 检查 systemd 服务文件
- 检查配置文件
- 检查手册页

</details>

---

## grep

<details>
<summary><b>grep — 13 个用例 / 44 个功能点</b></summary>

#### test_grep_basic_pattern_matching

- Basic grep for Hello
- Verify multiple matches
- Grep from pipe
- Grep across multiple files

#### test_grep_case_insensitive_i

- Case insensitive grep
- Verify case insensitive matches
- Case sensitive: lowercase only matches lowercase

#### test_grep_invert_match_v

- Invert match: exclude Hello
- Verify inverted output contains other lines

#### test_grep_word_and_line_matching_w_x

- Create word test file
- Add line with separate words
- Whole word match: hello matches only standalone
- Create line test file
- Add different line
- Whole line exact match

#### test_grep_count_and_line_numbers_c_n

- Count matches with -c
- Verify count >= 2
- Show line numbers with -n
- Verify line number format

#### test_grep_recursive_search_r

- Recursive grep in subdirectory
- Recursive list files with matches
- Recursive with --include filter

#### test_grep_extended_regex_e

- Extended regex with alternation
- Extended regex: digit quantifier
- Verify digit match count
- egrep equivalent to grep -E

#### test_grep_fixed_strings_f

- Fixed string with special chars
- Fixed string: no regex meta-char interpretation
- fgrep equivalent to grep -F

#### test_grep_only_matching_and_quiet_o_q

- Only matching: digits only
- Quiet mode: pattern found
- Quiet mode: pattern not found

#### test_grep_context_lines_a_b_c

- Context: 1 line after match
- Context: 1 line before match
- Context: 1 line before and after

#### test_grep_file_listing_l_l

- List files with matches
- List files without matches

#### test_grep_multiple_patterns_e_f

- Multiple patterns with -e
- Patterns from file with -f
- Max count: stop after first match

#### test_grep_error_handling

- Error on nonexistent file
- Error on invalid regex
- Error on directory without -r
- No match returns exit code 1

</details>

---

## groff

<details>
<summary><b>groff — 2 个用例 / 3 个功能点</b></summary>

#### test_groff_groff_basic

- 检查主要工具可执行性

#### test_groff_groff_version

- 获取 groff 帮助信息
- 获取 groff 版本信息

</details>

---

## gzip

<details>
<summary><b>gzip — 2 个用例 / 29 个功能点</b></summary>

#### test_gzip_version_help

- gzip 版本信息
- gzip 帮助信息
- gunzip 版本信息
- gunzip 帮助信息
- zcat 版本信息
- zcat 帮助信息
- zcmp 版本信息
- zcmp 帮助信息
- zdiff 版本信息
- zdiff 帮助信息
- zgrep 版本信息
- zgrep 帮助信息
- zless 版本信息
- zless 帮助信息
- zmore 版本信息
- zmore 帮助信息
- znew 版本信息
- znew 帮助信息
- gzexe 版本信息
- gzexe 帮助信息
- zforce 版本信息
- zforce 帮助信息
- zegrep 版本信息
- zegrep 帮助信息
- zfgrep 版本信息
- zfgrep 帮助信息
- uncompress 版本信息
- uncompress 帮助信息

#### test_gzip_error_handling

- gzip: 无效选项

</details>

---

## help2man

<details>
<summary><b>help2man — 2 个用例 / 3 个功能点</b></summary>

#### test_help2man_help2man_basic

- 检查主要工具可执行性

#### test_help2man_help2man_version

- 获取 help2man 帮助信息
- 获取 help2man 版本信息

</details>

---

## icu4c

<details>
<summary><b>icu4c — 1 个用例 / 1 个功能点</b></summary>

#### test_icu4c_basic_check

- 检查 icu4c 已安装

</details>

---

## iproute2

<details>
<summary><b>iproute2 — 1 个用例 / 1 个功能点</b></summary>

#### test_iproute2_basic_check

- 检查 iproute2 已安装

</details>

---

## iptables

<details>
<summary><b>iptables — 2 个用例 / 3 个功能点</b></summary>

#### test_iptables_iptables_basic

- 检查主要工具可执行性

#### test_iptables_iptables_version

- 获取 iptables 帮助信息
- 获取 iptables 版本信息

</details>

---

## iputils

<details>
<summary><b>iputils — 10 个用例 / 33 个功能点</b></summary>

#### test_iputils_ping_basic_functionality

- Ping localhost
- Ping with count limit
- Ping with interval
- Ping with packet size
- Ping with timeout

#### test_iputils_ping_advanced_options

- Ping with flood mode (requires root)
- Ping with numeric output
- Ping with quiet mode
- Ping with verbose output
- Ping with timestamp

#### test_iputils_ping6_ipv6

- Ping6 localhost
- Ping6 with count

#### test_iputils_traceroute6

- Basic traceroute6 to localhost
- traceroute6 with max hops
- traceroute6 with wait time

#### test_iputils_tracepath

- Basic tracepath to localhost
- tracepath with max hops
- tracepath IPv6

#### test_iputils_arping

- ARP ping to localhost interface
- arping with count
- arping with timeout

#### test_iputils_clockdiff

- Clock difference to localhost
- clockdiff with IPv6

#### test_iputils_ping_error_handling

- Ping unreachable address
- Ping with invalid address
- Ping with invalid count
- Ping with negative count

#### test_iputils_ping_special_scenarios

- Ping broadcast address (may require special permissions)
- Ping with source address
- Ping with TTL
- Continuous ping (limited by timeout)

#### test_iputils_network_interface_testing

- Ping via specific interface
- Multiple ping instances

</details>

---

## isl

<details>
<summary><b>isl — 1 个用例 / 2 个功能点</b></summary>

#### test_isl_version_help

- 列出包文件
- 库文件检查

</details>

---

## iso-codes

<details>
<summary><b>iso-codes — 1 个用例 / 1 个功能点</b></summary>

#### test_iso_codes_main

- 检查包已安装

</details>

---

## jitterentropy

<details>
<summary><b>jitterentropy — 1 个用例 / 2 个功能点</b></summary>

#### test_jitterentropy_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## json-c

<details>
<summary><b>json-c — 1 个用例 / 2 个功能点</b></summary>

#### test_json_c_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## kbd

<details>
<summary><b>kbd — 1 个用例 / 1 个功能点</b></summary>

#### test_kbd_basic_check

- 检查 kbd 已安装

</details>

---

## keyutils

<details>
<summary><b>keyutils — 1 个用例 / 1 个功能点</b></summary>

#### test_keyutils_basic_check

- 检查 keyutils 已安装

</details>

---

## kmod

<details>
<summary><b>kmod — 1 个用例 / 1 个功能点</b></summary>

#### test_kmod_basic_check

- 检查 kmod 已安装

</details>

---

## krb5

<details>
<summary><b>krb5 — 1 个用例 / 1 个功能点</b></summary>

#### test_krb5_basic_check

- 检查 krb5 已安装

</details>

---

## kyua

<details>
<summary><b>kyua — 2 个用例 / 3 个功能点</b></summary>

#### test_kyua_kyua_basic

- 检查主要工具可执行性

#### test_kyua_kyua_version

- 获取 kyua 帮助信息
- 获取 kyua 版本信息

</details>

---

## labwc

<details>
<summary><b>labwc — 9 个用例 / 10 个功能点</b></summary>

#### test_labwc_help

- labwc help

#### test_labwc_configuration

- labwc: config options

#### test_labwc_debug_mode

- labwc: debug option

#### test_labwc_check_for_display_no_display

- labwc: startup/session options

#### test_labwc_library_check

- labwc: linked libraries

#### test_labwc_labnag

- labnag help

#### test_labwc_labsensibleterminal

- lab-sensible-terminal help

#### test_labwc_config_dirs

- System config dir
- Data dir

#### test_labwc_error_handling

- labwc: invalid option

</details>

---

## less

<details>
<summary><b>less — 1 个用例 / 3 个功能点</b></summary>

#### test_less_main

- 获取 less 版本信息
- 获取 lessecho 版本信息
- 获取 lesskey 版本信息

</details>

---

## libaio

<details>
<summary><b>libaio — 1 个用例 / 2 个功能点</b></summary>

#### test_libaio_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libarchive

<details>
<summary><b>libarchive — 1 个用例 / 2 个功能点</b></summary>

#### test_libarchive_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libbpf

<details>
<summary><b>libbpf — 1 个用例 / 2 个功能点</b></summary>

#### test_libbpf_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libcap

<details>
<summary><b>libcap — 1 个用例 / 2 个功能点</b></summary>

#### test_libcap_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libcap-ng

<details>
<summary><b>libcap-ng — 1 个用例 / 2 个功能点</b></summary>

#### test_libcap_ng_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libeconf

<details>
<summary><b>libeconf — 1 个用例 / 2 个功能点</b></summary>

#### test_libeconf_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libedit

<details>
<summary><b>libedit — 1 个用例 / 2 个功能点</b></summary>

#### test_libedit_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libevent

<details>
<summary><b>libevent — 1 个用例 / 2 个功能点</b></summary>

#### test_libevent_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libffi

<details>
<summary><b>libffi — 1 个用例 / 2 个功能点</b></summary>

#### test_libffi_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libgcrypt

<details>
<summary><b>libgcrypt — 1 个用例 / 2 个功能点</b></summary>

#### test_libgcrypt_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libgpg-error

<details>
<summary><b>libgpg-error — 1 个用例 / 2 个功能点</b></summary>

#### test_libgpg_error_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libidn2

<details>
<summary><b>libidn2 — 1 个用例 / 1 个功能点</b></summary>

#### test_libidn2_main

- 获取 idn2 版本信息

</details>

---

## libmicrohttpd

<details>
<summary><b>libmicrohttpd — 1 个用例 / 4 个功能点</b></summary>

#### test_libmicrohttpd_main

- 获取 libmicrohttpd 版本信息
- 列出 libmicrohttpd 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## libmnl

<details>
<summary><b>libmnl — 1 个用例 / 2 个功能点</b></summary>

#### test_libmnl_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libnetfilter_conntrack

<details>
<summary><b>libnetfilter_conntrack — 1 个用例 / 2 个功能点</b></summary>

#### test_libnetfilter_conntrack_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libnfnetlink

<details>
<summary><b>libnfnetlink — 1 个用例 / 2 个功能点</b></summary>

#### test_libnfnetlink_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libnftnl

<details>
<summary><b>libnftnl — 1 个用例 / 2 个功能点</b></summary>

#### test_libnftnl_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libnl

<details>
<summary><b>libnl — 1 个用例 / 2 个功能点</b></summary>

#### test_libnl_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libpcap

<details>
<summary><b>libpcap — 1 个用例 / 4 个功能点</b></summary>

#### test_libpcap_main

- 获取 libpcap 版本信息
- 列出 libpcap 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## libpng

<details>
<summary><b>libpng — 1 个用例 / 1 个功能点</b></summary>

#### test_libpng_main

- 获取 pngfix 版本信息

</details>

---

## libpsl

<details>
<summary><b>libpsl — 1 个用例 / 2 个功能点</b></summary>

#### test_libpsl_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libpwquality

<details>
<summary><b>libpwquality — 1 个用例 / 2 个功能点</b></summary>

#### test_libpwquality_main

- 获取 pwmake 版本信息
- 获取 pwscore 版本信息

</details>

---

## libseccomp

<details>
<summary><b>libseccomp — 1 个用例 / 2 个功能点</b></summary>

#### test_libseccomp_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libselinux

<details>
<summary><b>libselinux — 1 个用例 / 2 个功能点</b></summary>

#### test_libselinux_version_help

- 列出包文件
- 库文件检查

</details>

---

## libsepol

<details>
<summary><b>libsepol — 1 个用例 / 2 个功能点</b></summary>

#### test_libsepol_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libsodium

<details>
<summary><b>libsodium — 1 个用例 / 4 个功能点</b></summary>

#### test_libsodium_main

- 获取 libsodium 版本信息
- 列出 libsodium 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## libssh

<details>
<summary><b>libssh — 1 个用例 / 4 个功能点</b></summary>

#### test_libssh_main

- 获取 libssh 版本信息
- 列出 libssh 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## libtasn1

<details>
<summary><b>libtasn1 — 1 个用例 / 3 个功能点</b></summary>

#### test_libtasn1_main

- 获取 asn1Coding 版本信息
- 获取 asn1Decoding 版本信息
- 获取 asn1Parser 版本信息

</details>

---

## libtirpc

<details>
<summary><b>libtirpc — 1 个用例 / 2 个功能点</b></summary>

#### test_libtirpc_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libtool

<details>
<summary><b>libtool — 2 个用例 / 3 个功能点</b></summary>

#### test_libtool_libtool

- 检查主要工具可执行性

#### test_libtool_libtool

- 获取 libtool 帮助信息
- 获取 libtool 版本信息

</details>

---

## libunistring

<details>
<summary><b>libunistring — 1 个用例 / 2 个功能点</b></summary>

#### test_libunistring_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libxcrypt

<details>
<summary><b>libxcrypt — 1 个用例 / 2 个功能点</b></summary>

#### test_libxcrypt_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## libxml2

<details>
<summary><b>libxml2 — 1 个用例 / 2 个功能点</b></summary>

#### test_libxml2_main

- 获取 xmlcatalog 版本信息
- 获取 xmllint 版本信息

</details>

---

## libxslt

<details>
<summary><b>libxslt — 1 个用例 / 1 个功能点</b></summary>

#### test_libxslt_main

- 获取 xsltproc 版本信息

</details>

---

## linux-headers

<details>
<summary><b>linux-headers — 1 个用例 / 2 个功能点</b></summary>

#### test_linux_headers_version_help

- 列出包文件
- 库文件检查

</details>

---

## lua

<details>
<summary><b>lua — 2 个用例 / 5 个功能点</b></summary>

#### test_lua_version_help

- lua 版本信息
- lua 帮助信息
- luac 版本信息
- luac 帮助信息

#### test_lua_error_handling

- lua: 无效选项

</details>

---

## lutok

<details>
<summary><b>lutok — 1 个用例 / 4 个功能点</b></summary>

#### test_lutok_main

- 获取 lutok 版本信息
- 列出 lutok 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## lvm2

<details>
<summary><b>lvm2 — 1 个用例 / 1 个功能点</b></summary>

#### test_lvm2_basic_check

- 检查 lvm2 已安装

</details>

---

## lz4

<details>
<summary><b>lz4 — 1 个用例 / 4 个功能点</b></summary>

#### test_lz4_main

- 获取 lz4 版本信息
- 获取 lz4c 版本信息
- 获取 lz4cat 版本信息
- 获取 unlz4 版本信息

</details>

---

## lzip

<details>
<summary><b>lzip — 2 个用例 / 3 个功能点</b></summary>

#### test_lzip_lzip_basic

- 检查主要工具可执行性

#### test_lzip_lzip_version

- 获取 lzip 帮助信息
- 获取 lzip 版本信息

</details>

---

## make

<details>
<summary><b>make — 9 个用例 / 21 个功能点</b></summary>

#### test_make_basic_makefile_execution

- Run default target
- Run specific target
- Run clean target
- make -s: silent mode

#### test_make_variables

- Variable expansion
- Override variable

#### test_make_options

- make -n: dry run
- make -B: always make
- make --just-print
- make -d: debug output
- make --debug=b: basic debug
- make -q: question mode
- make -s: silent

#### test_make_parallel_execution

- make -j2: parallel 2 jobs

#### test_make_environment

- make -e: environment overrides
- Environment variable in make

#### test_make_directory_change

- make -C: change directory

#### test_make_include

- Include file

#### test_make_gmake_alias

- gmake is GNU Make

#### test_make_error_handling

- make -k: continue on error
- make -i: ignore errors

</details>

---

## meson

<details>
<summary><b>meson — 1 个用例 / 4 个功能点</b></summary>

#### test_meson_main

- 获取 meson 版本信息
- 列出包内二进制文件
- 获取 meson 版本输出
- 检查手册页

</details>

---

## mpc

<details>
<summary><b>mpc — 1 个用例 / 2 个功能点</b></summary>

#### test_mpc_version_help

- 列出包文件
- 库文件检查

</details>

---

## mpdecimal

<details>
<summary><b>mpdecimal — 1 个用例 / 2 个功能点</b></summary>

#### test_mpdecimal_version_help

- 列出包文件
- 库文件检查

</details>

---

## mpfr

<details>
<summary><b>mpfr — 1 个用例 / 2 个功能点</b></summary>

#### test_mpfr_version_help

- 列出包文件
- 库文件检查

</details>

---

## ncurses

<details>
<summary><b>ncurses — 1 个用例 / 1 个功能点</b></summary>

#### test_ncurses_basic_check

- 检查 ncurses 已安装

</details>

---

## nettle

<details>
<summary><b>nettle — 2 个用例 / 11 个功能点</b></summary>

#### test_nettle_version_help

- nettle-hash 版本信息
- nettle-hash 帮助信息
- nettle-lfib-stream 版本信息
- nettle-lfib-stream 帮助信息
- nettle-pbkdf2 版本信息
- nettle-pbkdf2 帮助信息
- pkcs1-conv 版本信息
- pkcs1-conv 帮助信息
- sexp-conv 版本信息
- sexp-conv 帮助信息

#### test_nettle_error_handling

- nettle-hash: 无效选项

</details>

---

## newt

<details>
<summary><b>newt — 2 个用例 / 3 个功能点</b></summary>

#### test_newt_version_help

- whiptail 版本信息
- whiptail 帮助信息

#### test_newt_error_handling

- whiptail: 无效选项

</details>

---

## nfs-utils

<details>
<summary><b>nfs-utils — 1 个用例 / 5 个功能点</b></summary>

#### test_nfs_utils_main

- 获取 nfs-utils 版本信息
- 列出包内二进制文件
- 检查 systemd 服务文件
- 检查配置文件
- 检查手册页

</details>

---

## nghttp2

<details>
<summary><b>nghttp2 — 1 个用例 / 2 个功能点</b></summary>

#### test_nghttp2_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## ninja

<details>
<summary><b>ninja — 1 个用例 / 4 个功能点</b></summary>

#### test_ninja_main

- 获取 ninja 版本信息
- 列出包内二进制文件
- 获取 ninja 版本输出
- 检查手册页

</details>

---

## nss

<details>
<summary><b>nss — 2 个用例 / 3 个功能点</b></summary>

#### test_nss_nss

- 检查主要工具可执行性

#### test_nss_nss

- 获取 nss 帮助信息
- 获取 nss 版本信息

</details>

---

## nss_wrapper

<details>
<summary><b>nss_wrapper — 1 个用例 / 4 个功能点</b></summary>

#### test_nss_wrapper_main

- 获取 nss_wrapper 版本信息
- 列出 nss_wrapper 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## openruyi-release

<details>
<summary><b>openruyi-release — 1 个用例 / 1 个功能点</b></summary>

#### test_openruyi_release_main

- 检查包已安装

</details>

---

## openssh

<details>
<summary><b>openssh — 1 个用例 / 1 个功能点</b></summary>

#### test_openssh_main

- 获取 ssh 版本信息

</details>

---

## openssh-clients

<details>
<summary><b>openssh-clients — 7 个用例 / 19 个功能点</b></summary>

#### test_openssh_clients_ssh_version_and_help

- ssh version
- ssh -Q key: supported keys
- ssh -Q cipher: ciphers
- ssh -Q mac: MACs
- ssh -Q kex: key exchange

#### test_openssh_clients_ssh_connection_dryrun

- ssh -G: print config
- ssh -T: disable PTY
- ssh -v: verbose

#### test_openssh_clients_sshkeygen_via_openssh

- Generate test key

#### test_openssh_clients_sshagent

- ssh-add: list keys
- ssh-add: add key
- ssh-add: verify key added
- ssh-add -L: list public keys
- ssh-add -d: remove key

#### test_openssh_clients_sshkeyscan

- ssh-keyscan: scan localhost
- ssh-keyscan -t rsa
- ssh-keyscan -t ecdsa

#### test_openssh_clients_sftp

- sftp: help command

#### test_openssh_clients_scp

- scp version

</details>

---

## openssl

<details>
<summary><b>openssl — 1 个用例 / 1 个功能点</b></summary>

#### test_openssl_main

- 获取 openssl 版本信息

</details>

---

## p11-kit

<details>
<summary><b>p11-kit — 1 个用例 / 1 个功能点</b></summary>

#### test_p11_kit_basic_check

- 检查 p11-kit 已安装

</details>

---

## pam

<details>
<summary><b>pam — 2 个用例 / 11 个功能点</b></summary>

#### test_pam_version_help

- faillock 版本信息
- faillock 帮助信息
- mkhomedir_helper 版本信息
- mkhomedir_helper 帮助信息
- pam_timestamp_check 版本信息
- pam_timestamp_check 帮助信息
- unix_chkpwd 版本信息
- unix_chkpwd 帮助信息
- unix_update 版本信息
- unix_update 帮助信息

#### test_pam_error_handling

- faillock: 无效选项

</details>

---

## patch

<details>
<summary><b>patch — 1 个用例 / 1 个功能点</b></summary>

#### test_patch_main

- 获取 patch 版本信息

</details>

---

## pciutils

<details>
<summary><b>pciutils — 13 个用例 / 13 个功能点</b></summary>

#### test_pciutils_lspci_basic

- test_pciutils_lspci_basic

#### test_pciutils_lspci_verbose

- test_pciutils_lspci_verbose

#### test_pciutils_lspci_with_filtering

- test_pciutils_lspci_with_filtering

#### test_pciutils_lspci_numeric

- test_pciutils_lspci_numeric

#### test_pciutils_lspci_tree_view

- test_pciutils_lspci_tree_view

#### test_pciutils_lspci_kernel_drivers

- test_pciutils_lspci_kernel_drivers

#### test_pciutils_lspci_by_device_class

- test_pciutils_lspci_by_device_class

#### test_pciutils_lspci_with_domain

- test_pciutils_lspci_with_domain

#### test_pciutils_updatepciids

- test_pciutils_updatepciids

#### test_pciutils_lspci_format_options

- test_pciutils_lspci_format_options

#### test_pciutils_setpci

- test_pciutils_setpci

#### test_pciutils_pcilmr

- test_pciutils_pcilmr

#### test_pciutils_error_handling

- test_pciutils_error_handling

</details>

---

## pcre2

<details>
<summary><b>pcre2 — 1 个用例 / 2 个功能点</b></summary>

#### test_pcre2_main

- 获取 pcre2grep 版本信息
- 获取 pcre2test 版本信息

</details>

---

## perl

<details>
<summary><b>perl — 1 个用例 / 1 个功能点</b></summary>

#### test_perl_main

- 获取 perl 版本信息

</details>

---

## perl-Error

<details>
<summary><b>perl-Error — 1 个用例 / 4 个功能点</b></summary>

#### test_perl_error_main

- 获取 perl-Error 版本信息
- 加载 perl-Error Perl 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## perl-Locale-gettext

<details>
<summary><b>perl-Locale-gettext — 1 个用例 / 4 个功能点</b></summary>

#### test_perl_locale_gettext_main

- 获取 perl-Locale-gettext 版本信息
- 加载 perl-Locale-gettext Perl 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## perl-rpm-packaging

<details>
<summary><b>perl-rpm-packaging — 1 个用例 / 4 个功能点</b></summary>

#### test_perl_rpm_packaging_main

- 获取 perl-rpm-packaging 版本信息
- 加载 perl-rpm-packaging Perl 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## pkgconf

<details>
<summary><b>pkgconf — 2 个用例 / 5 个功能点</b></summary>

#### test_pkgconf_version_help

- pkgconf 版本信息
- pkgconf 帮助信息
- bomtool 版本信息
- bomtool 帮助信息

#### test_pkgconf_error_handling

- pkgconf: 无效选项

</details>

---

## podman

<details>
<summary><b>podman — 7 个用例 / 16 个功能点</b></summary>

#### test_podman_image_operations

- podman images: list images
- podman image list

#### test_podman_container_operations

- podman ps: list containers
- podman ps -a: all containers
- podman container list

#### test_podman_network_operations

- podman network ls
- podman network inspect

#### test_podman_volume_operations

- podman volume ls

#### test_podman_system_operations

- podman system info
- podman system df: disk usage

#### test_podman_help_commands

- podman manifest help
- podman healthcheck help
- podman events help
- podman pod list
- podman-remote help

#### test_podman_error_handling

- podman: invalid command

</details>

---

## podmansh

<details>
<summary><b>podmansh — 11 个用例 / 11 个功能点</b></summary>

#### test_podmansh_podmansh_basic

- test_podmansh_podmansh_basic

#### test_podmansh_podmansh_help

- test_podmansh_podmansh_help

#### test_podmansh_podmansh_config

- test_podmansh_podmansh_config

#### test_podmansh_podman_basic

- test_podmansh_podman_basic

#### test_podmansh_podman_images

- test_podmansh_podman_images

#### test_podmansh_podman_network

- test_podmansh_podman_network

#### test_podmansh_podman_volume

- test_podmansh_podman_volume

#### test_podmansh_podman_stats

- test_podmansh_podman_stats

#### test_podmansh_podman_ps

- test_podmansh_podman_ps

#### test_podmansh_error_handling

- test_podmansh_error_handling

#### test_podmansh_cleanup

- test_podmansh_cleanup

</details>

---

## popt

<details>
<summary><b>popt — 1 个用例 / 2 个功能点</b></summary>

#### test_popt_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## procps-ng

<details>
<summary><b>procps-ng — 14 个用例 / 53 个功能点</b></summary>

#### test_procps_ng_ps_command_basic_functionality

- Basic ps output
- ps with full format
- ps with custom format
- ps showing all processes
- ps with tree view

#### test_procps_ng_ps_command_advanced_features

- Filter by user
- Filter by PID
- Show threads
- Process hierarchy
- Sort by CPU usage
- Sort by memory usage

#### test_procps_ng_free_command

- Basic memory info
- Human-readable format
- Display in different units
- Continuous monitoring (single iteration)
- Show total column
- Show low/high memory

#### test_procps_ng_top_command

- Basic top (batch mode, single iteration)
- Top with specific number of processes
- Top sorted by memory
- Top with delay

#### test_procps_ng_vmstat_command

- Basic vmstat output
- vmstat with custom intervals
- vmstat with slabs info
- vmstat with disk stats
- vmstat with partitions

#### test_procps_ng_uptime_and_w_commands

- System uptime
- Show users
- Show who is logged in

#### test_procps_ng_kill_command

- Start a background process
- List signal numbers
- Send SIGTERM
- Wait for process to terminate
- Verify process terminated

#### test_procps_ng_pidof_and_pgrep

- Find PID by name
- pgrep basic usage
- pgrep with full command line

#### test_procps_ng_pwdx_and_pmap

- Show process working directory
- Show process memory map

#### test_procps_ng_sysctl_if_available

- List all sysctl parameters
- Read specific parameter

#### test_procps_ng_error_handling

- ps with invalid PID
- kill with invalid PID
- free with invalid option

#### test_procps_ng_special_scenarios

- ps with environment variables
- Process with real-time priority
- Show process namespaces

#### test_procps_ng_pkill_and_pidwait

- pkill version check
- pidwait version check

#### test_procps_ng_slabtop_tload_watch_hugetop

- slabtop display
- tload version
- watch basic usage
- hugetop

</details>

---

## psmisc

<details>
<summary><b>psmisc — 13 个用例 / 22 个功能点</b></summary>

#### test_psmisc_fuser_basic

- Test fuser on /tmp

#### test_psmisc_fuser_with_processes

- Show processes using /tmp

#### test_psmisc_fuser_mount_points

- test_psmisc_fuser_mount_points

#### test_psmisc_fuser_with_options

- test_psmisc_fuser_with_options

#### test_psmisc_pstree_basic

- test_psmisc_pstree_basic

#### test_psmisc_pstree_with_options

- Show PIDs
- Show numeric sort
- Compact tree
- Highlight current process
- Show full details
- Show only one user's processes

#### test_psmisc_killall_basic

- Start test process
- Try killall (may not kill itself)
- Clean up

#### test_psmisc_prtstat

- test_psmisc_prtstat

#### test_psmisc_peekfd

- test_psmisc_peekfd

#### test_psmisc_pslog

- test_psmisc_pslog

#### test_psmisc_killall_with_signals

- List signal names
- Test signal send

#### test_psmisc_fuser_special_cases

- fuser on unix socket
- fuser reset signal output

#### test_psmisc_error_handling

- test_psmisc_error_handling

</details>

---

## publicsuffix-list

<details>
<summary><b>publicsuffix-list — 1 个用例 / 1 个功能点</b></summary>

#### test_publicsuffix_list_main

- 检查包已安装

</details>

---

## pyproject-rpm-macros

<details>
<summary><b>pyproject-rpm-macros — 1 个用例 / 1 个功能点</b></summary>

#### test_pyproject_rpm_macros_main

- 检查包已安装

</details>

---

## python

<details>
<summary><b>python — 5 个用例 / 8 个功能点</b></summary>

#### test_python_basic_execution

- Python 基本运算
- Python sys模块

#### test_python_basic

- python3 -h: 帮助
- python3 -V: 版本
- python3: os模块

#### test_python_basic

- python3 执行脚本

#### test_python_basic

- python3: 导入标准模块

#### test_python_error_handling

- python3: 导入错误

</details>

---

## python-flit-core

<details>
<summary><b>python-flit-core — 1 个用例 / 4 个功能点</b></summary>

#### test_python_flit_core_main

- 获取 python-flit-core 版本信息
- 导入 python-flit-core Python 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## python-lxml

<details>
<summary><b>python-lxml — 1 个用例 / 2 个功能点</b></summary>

#### test_python_lxml_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## python-packaging

<details>
<summary><b>python-packaging — 1 个用例 / 1 个功能点</b></summary>

#### test_python_packaging_main

- 检查包已安装

</details>

---

## python-pip

<details>
<summary><b>python-pip — 1 个用例 / 1 个功能点</b></summary>

#### test_python_pip_main

- 获取 pip3 版本信息

</details>

---

## python-pyelftools

<details>
<summary><b>python-pyelftools — 1 个用例 / 4 个功能点</b></summary>

#### test_python_pyelftools_main

- 获取 python-pyelftools 版本信息
- 导入 python-pyelftools Python 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## python-rpm-generators

<details>
<summary><b>python-rpm-generators — 1 个用例 / 4 个功能点</b></summary>

#### test_python_rpm_generators_main

- 获取 python-rpm-generators 版本信息
- 导入 python-rpm-generators Python 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## python-rpm-macros

<details>
<summary><b>python-rpm-macros — 1 个用例 / 1 个功能点</b></summary>

#### test_python_rpm_macros_main

- 检查包已安装

</details>

---

## python-setuptools

<details>
<summary><b>python-setuptools — 1 个用例 / 4 个功能点</b></summary>

#### test_python_setuptools_main

- 获取 python-setuptools 版本信息
- 导入 python-setuptools Python 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## python-srpm-macros

<details>
<summary><b>python-srpm-macros — 1 个用例 / 1 个功能点</b></summary>

#### test_python_srpm_macros_main

- 检查包已安装

</details>

---

## python-wheel

<details>
<summary><b>python-wheel — 1 个用例 / 4 个功能点</b></summary>

#### test_python_wheel_main

- 获取 python-wheel 版本信息
- 导入 python-wheel Python 模块
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## re2c

<details>
<summary><b>re2c — 2 个用例 / 3 个功能点</b></summary>

#### test_re2c_re2c_basic

- 检查主要工具可执行性

#### test_re2c_re2c_version

- 获取 re2c 帮助信息
- 获取 re2c 版本信息

</details>

---

## readline

<details>
<summary><b>readline — 1 个用例 / 2 个功能点</b></summary>

#### test_readline_main

- 查找 .so 库文件
- 检查包已安装

</details>

---

## rpm

<details>
<summary><b>rpm — 1 个用例 / 1 个功能点</b></summary>

#### test_rpm_main

- rpm 锟芥本

</details>

---

## rpm-config-openruyi

<details>
<summary><b>rpm-config-openruyi — 1 个用例 / 2 个功能点</b></summary>

#### test_rpm_config_openruyi_version_help

- 列出包文件
- 库文件检查

</details>

---

## rpmbuild

<details>
<summary><b>rpmbuild — 9 个用例 / 20 个功能点</b></summary>

#### test_rpmbuild_rpmbuild_basic_functionality

- Check rpmbuild version
- Setup RPM build tree

#### test_rpmbuild_create_simple_spec_file

- Create minimal spec file

#### test_rpmbuild_create_source_tarball

- Create test source
- Verify source file

#### test_rpmbuild_build_rpm_package

- Build binary RPM
- Build source RPM

#### test_rpmbuild_verify_built_rpm

- Query RPM info
- Verify RPM dependencies
- Check RPM provides

#### test_rpmbuild_install_and_test_rpm

- Install the RPM (test mode)
- Actually install
- Verify installation

#### test_rpmbuild_rpm_build_options

- Build with --define
- Check build log

#### test_rpmbuild_error_handling

- Build with missing spec file
- Build with missing source

#### test_rpmbuild_rpm_verification

- Verify RPM signature (may not be signed)
- Check RPM integrity
- Cleanup

</details>

---

## rsync

<details>
<summary><b>rsync — 2 个用例 / 3 个功能点</b></summary>

#### test_rsync_rsync_basic

- 检查主要工具可执行性

#### test_rsync_rsync_version

- 获取 rsync 帮助信息
- 获取 rsync 版本信息

</details>

---

## scdoc

<details>
<summary><b>scdoc — 2 个用例 / 3 个功能点</b></summary>

#### test_scdoc_scdoc_basic

- 检查主要工具可执行性

#### test_scdoc_scdoc_version

- 获取 scdoc 帮助信息
- 获取 scdoc 版本信息

</details>

---

## sddm

<details>
<summary><b>sddm — 5 个用例 / 10 个功能点</b></summary>

#### test_sddm_version_and_help

- sddm help
- sddm --test-mode help

#### test_sddm_configuration

- sddm: example config
- Config directory
- Default config dir

#### test_sddm_service_check

- sddm service unit
- sddm service status
- sddm enabled status

#### test_sddm_theme_check

- sddm themes installed

#### test_sddm_config_values

- sddm: key config values

</details>

---

## sed

<details>
<summary><b>sed — 6 个用例 / 12 个功能点</b></summary>

#### test_sed_basic_substitution

- sed s: 基本替换
- sed s: 替换hello

#### test_sed_line_operations

- sed -n: 打印指定行
- sed d: 删除指定行
- sed a: 追加行
- sed i: 插入行

#### test_sed_global_regex

- sed g: 全局替换
- sed: 正则替换

#### test_sed_basic

- sed -i: 就地编辑
- sed -i: 验证修改

#### test_sed_basic

- sed -e: 多表达式

#### test_sed_error_handling

- sed: 无效选项

</details>

---

## setup

<details>
<summary><b>setup — 1 个用例 / 1 个功能点</b></summary>

#### test_setup_main

- 检查包已安装

</details>

---

## slang

<details>
<summary><b>slang — 1 个用例 / 1 个功能点</b></summary>

#### test_slang_main

- 获取 slsh 版本信息

</details>

---

## socket_wrapper

<details>
<summary><b>socket_wrapper — 1 个用例 / 4 个功能点</b></summary>

#### test_socket_wrapper_main

- 获取 socket_wrapper 版本信息
- 列出 socket_wrapper 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## source-highlight

<details>
<summary><b>source-highlight — 2 个用例 / 3 个功能点</b></summary>

#### test_source_highlight_source_highlight_basic

- 检查主要工具可执行性

#### test_source_highlight_source_highlight_version

- 获取 source-highlight 帮助信息
- 获取 source-highlight 版本信息

</details>

---

## sqlite

<details>
<summary><b>sqlite — 1 个用例 / 2 个功能点</b></summary>

#### test_sqlite_main

- 获取 sqldiff 版本信息
- 获取 sqlite3 版本信息

</details>

---

## swig

<details>
<summary><b>swig — 2 个用例 / 3 个功能点</b></summary>

#### test_swig_swig_basic

- 检查主要工具可执行性

#### test_swig_swig_version

- 获取 swig 帮助信息
- 获取 swig 版本信息

</details>

---

## systemd

<details>
<summary><b>systemd — 36 个用例 / 114 个功能点</b></summary>

#### test_systemd_systemctl_service_and_system_management

- systemctl version
- systemctl: list running services
- systemctl: list targets
- systemctl --all: all services
- systemctl: list unit files
- systemctl is-active: check service status
- systemctl is-enabled: check enabled
- systemctl is-failed: list failed units
- systemctl status: service status
- systemctl show: service properties
- systemctl cat: show unit file
- systemctl list-dependencies
- systemctl list-sockets
- systemctl list-timers
- systemctl list-machines

#### test_systemd_journalctl_journal_query

- journalctl version
- journalctl -n: last entries
- journalctl -b: current boot
- journalctl --list-boots
- journalctl -k: kernel messages
- journalctl -o short: short format
- journalctl -o json: json format
- journalctl -o verbose
- journalctl --disk-usage
- journalctl --output=cat
- journalctl -p err: error messages
- journalctl --since
- journalctl -q: quiet

#### test_systemd_systemdanalyze_system_profiling

- systemd-analyze version
- systemd-analyze time: boot time
- systemd-analyze security

#### test_systemd_hostnamectl_hostname_management

- hostnamectl version
- hostnamectl status: system info
- hostnamectl hostname: current name
- hostnamectl --static
- hostnamectl --transient
- hostnamectl --pretty
- hostnamectl chassis

#### test_systemd_localectl_locale_management

- localectl version
- localectl status: locale info
- localectl list-locales

#### test_systemd_timedatectl_timedate_management

- timedatectl version
- timedatectl status: time info
- timedatectl show: all properties
- timedatectl list-timezones
- timedatectl show-timesync

#### test_systemd_loginctl_login_management

- loginctl version
- loginctl list-sessions
- loginctl list-users
- loginctl show-session
- loginctl show-user
- loginctl user-status

#### test_systemd_systemddetectvirt

- systemd-detect-virt: detect VM
- systemd-detect-virt -q: quiet mode
- systemd-detect-virt -c: container only
- systemd-detect-virt -v: VM only
- systemd-detect-virt -r: chroot only

#### test_systemd_systemdcgls_cgroup_listing

- systemd-cgls: cgroup tree
- systemd-cgls -k: kernel threads
- systemd-cgls --no-pager

#### test_systemd_systemdcgtop_cgroup_top

- systemd-cgtop -b: batch mode

#### test_systemd_systemdtmpfiles

- systemd-tmpfiles version
- systemd-tmpfiles --cat-config

#### test_systemd_busctl_dbus_introspection

- busctl version
- busctl list: list services
- busctl status: bus status
- busctl tree: object tree
- busctl introspect

#### test_systemd_systemdrun

- systemd-run version
- systemd-run --user --scope

#### test_systemd_systemdcat

- systemd-cat: pipe to journal
- systemd-cat version

#### test_systemd_systemdnotify

- systemd-notify version
- systemd-notify help

#### test_systemd_systemdpath

- systemd-path: all paths
- systemd-path: specific path
- systemd-path --suffix
- systemd-path help

#### test_systemd_systemdescape

- systemd-escape: basic escape
- systemd-escape --path: path escape
- systemd-escape -u: unescape
- systemd-escape --suffix
- systemd-escape --template

#### test_systemd_systemdmachineidsetup

- systemd-machine-id-setup help
- systemd-machine-id-setup: check machine-id

#### test_systemd_coredumpctl

- coredumpctl version
- coredumpctl list: list dumps
- coredumpctl info

#### test_systemd_systemddelta

- systemd-delta help
- systemd-delta: show overrides

#### test_systemd_systemdid128

- systemd-id128 show: show IDs
- systemd-id128 new: generate ID

#### test_systemd_systemdinhibit

- systemd-inhibit help
- systemd-inhibit --list

#### test_systemd_systemdacpower

- systemd-ac-power: check power

#### test_systemd_systemdaskpassword

- systemd-ask-password help

#### test_systemd_systemdcreds

- systemd-creds help

#### test_systemd_systemdsocketactivate

- systemd-socket-activate help

#### test_systemd_power_management_commands

- $cmd help

#### test_systemd_systemdfirstboot

- systemd-firstboot help

#### test_systemd_systemdstdiobridge

- systemd-stdio-bridge help

#### test_systemd_oomctl

- oomctl help
- oomctl dump

#### test_systemd_systemctl_service_operations

- systemctl try-restart
- systemctl reload-or-restart
- systemctl reset-failed
- systemctl daemon-reload

#### test_systemd_run0_privilege_escalation

- run0 help

#### test_systemd_systemdmount

- systemd-mount help

#### test_systemd_systemdsysext

- systemd-sysext help

#### test_systemd_systemdconfext

- systemd-confext help

#### test_systemd_error_handling

- systemctl: invalid command
- journalctl: invalid option
- hostnamectl: invalid option

</details>

---

## systemd-timesyncd

<details>
<summary><b>systemd-timesyncd — 5 个用例 / 13 个功能点</b></summary>

#### test_systemd_timesyncd_service_status

- Service status
- Time sync status
- Timesync detail
- Is enabled

#### test_systemd_timesyncd_ntp_management

- Fallback NTP servers
- Current NTP server
- Server address
- NTP servers list

#### test_systemd_timesyncd_service_control

- Restart service
- Is active

#### test_systemd_timesyncd_configuration

- Config file
- Cat config

#### test_systemd_timesyncd_systemdtimewaitsync

- Wait sync service

</details>

---

## systemtap

<details>
<summary><b>systemtap — 2 个用例 / 3 个功能点</b></summary>

#### test_systemtap_systemtap_basic

- 检查主要工具可执行性

#### test_systemtap_systemtap_version

- 获取 systemtap 帮助信息
- 获取 systemtap 版本信息

</details>

---

## tar

<details>
<summary><b>tar — 10 个用例 / 27 个功能点</b></summary>

#### test_tar_basic_archive_creation

- Create test files
- Create tar archive
- List archive contents

#### test_tar_archive_extraction

- Extract archive
- Verify extracted files

#### test_tar_compression_formats

- Create gzip compressed archive
- Create bzip2 compressed archive
- Create xz compressed archive
- Extract different formats

#### test_tar_advanced_tar_options

- Append files to existing archive
- Extract specific files
- Extract to different directory
- Create archive from directory

#### test_tar_archive_verification

- Test archive integrity
- Compare archive with original files

#### test_tar_special_attributes

- Preserve permissions
- Preserve timestamps

#### test_tar_error_handling

- Non-existent file
- Corrupted archive
- Empty archive

#### test_tar_wildcard_and_patterns

- Extract with wildcard pattern
- Exclude patterns

#### test_tar_incremental_backup

- Create incremental backup
- Multi-volume archive (test only)

#### test_tar_special_file_types

- Archive with symlinks
- Archive with hardlinks
- Cleanup

</details>

---

## tcl

<details>
<summary><b>tcl — 2 个用例 / 3 个功能点</b></summary>

#### test_tcl_tcl_basic

- 检查主要工具可执行性

#### test_tcl_tcl_version

- 获取 tcl 帮助信息
- 获取 tcl 版本信息

</details>

---

## tcsh

<details>
<summary><b>tcsh — 1 个用例 / 1 个功能点</b></summary>

#### test_tcsh_main

- 获取 tcsh 版本信息

</details>

---

## texinfo

<details>
<summary><b>texinfo — 2 个用例 / 3 个功能点</b></summary>

#### test_texinfo_texinfo_basic

- 检查主要工具可执行性

#### test_texinfo_texinfo_version

- 获取 texinfo 帮助信息
- 获取 texinfo 版本信息

</details>

---

## time

<details>
<summary><b>time — 1 个用例 / 1 个功能点</b></summary>

#### test_time_main

- 获取 time 版本信息

</details>

---

## tmux

<details>
<summary><b>tmux — 22 个用例 / 179 个功能点</b></summary>

#### test_tmux_server_management

- start-server: start tmux server
- list-sessions: initial state
- has-session: check nonexistent
- list-clients: list connected clients
- list-commands: list all commands
- list-commands: filter specific command
- list-commands: format output
- server-access -l: list access

#### test_tmux_session_creation_and_management

- new-session -d: create detached session
- has-session: verify session exists
- new-session -d: with start directory
- has-session: verify sess2 exists
- new-session -e: set environment
- new-session -F: format output
- new-session: set dimensions
- new-session -A: attach if exists
- list-sessions: list all sessions
- list-sessions -F: formatted
- rename-session: rename sess2
- has-session: verify renamed session
- lock-session: lock session
- switch-client -t: switch to session
- attach-session -d: attach and detach others
- detach-client -P
- detach-client -a: all in session
- suspend-client: suspend client
- lock-client: lock client
- refresh-client -S: status line only
- refresh-client -L: lease

#### test_tmux_window_management

- new-window: create window
- new-window -d: detached
- new-window -c: with directory
- new-window -e: with env
- list-windows: list all windows
- list-windows -a: all sessions
- list-windows -F: formatted
- select-window: by name
- select-window: by index
- select-window -l: last window
- select-window -n: next
- select-window -p: previous
- rename-window: rename window
- next-window: next
- previous-window: prev
- last-window: last
- move-window -a: after
- move-window -b: before
- swap-window
- link-window: link window
- unlink-window: unlink
- kill-window: create temp window
- kill-window: kill window
- rotate-window: rotate
- rotate-window -D: downward
- respawn-window -k: respawn
- resize-window: set size
- resize-window -U: up
- resize-window -D: down

#### test_tmux_pane_management

- split-window: horizontal split
- split-window -h: vertical split
- split-window -v: vertical explicit
- split-window -l: with size
- split-window -d: don't focus
- split-window -f: full size
- split-window -b: before
- split-window -I: create empty pane
- list-panes: list panes
- list-panes -as: all panes
- list-panes -F: formatted
- display-panes: show pane IDs
- select-pane: by ID
- select-pane -l: last pane
- select-pane -U: up
- select-pane -D: down
- select-pane -L: left
- select-pane -R: right
- resize-pane -y: height
- resize-pane -x: width
- resize-pane -U: up
- resize-pane -D: down
- resize-pane -L: left
- resize-pane -R: right
- resize-pane -Z: zoom
- break-pane -d: break pane to new window
- join-pane: join pane back
- move-pane: move pane
- swap-pane: swap panes
- last-pane: switch to last pane
- kill-pane: create temp pane
- kill-pane: kill pane
- kill-pane -a: kill all but current
- capture-pane -p: print to stdout
- capture-pane: range capture
- capture-pane -J: join lines
- pipe-pane -o: pipe output
- respawn-pane -k: respawn

#### test_tmux_layout_management

- select-layout: even-horizontal
- select-layout: even-vertical
- select-layout: main-horizontal
- select-layout: main-vertical
- select-layout: tiled
- next-layout: cycle layouts
- previous-layout: prev layout

#### test_tmux_buffer_management

- set-buffer -b: named buffer
- set-buffer: direct data
- set-buffer -a: append
- list-buffers: list all buffers
- list-buffers -F: formatted
- show-buffer: show buffer contents
- paste-buffer: paste buffer
- paste-buffer -d: delete after paste
- delete-buffer: create temp buffer
- delete-buffer: delete buffer
- save-buffer: create buffer
- save-buffer: save to file
- load-buffer: load from file

#### test_tmux_key_bindings_and_input

- list-keys: list all keys
- list-keys -T: prefix table
- list-keys -T: root table
- list-keys -a: all keys
- list-keys -N: with notes
- bind-key -n: bind to key
- unbind-key -n: unbind key
- bind-key -T: bind in table
- unbind-key -T: unbind in table
- send-keys: send text
- send-keys -l: literal
- send-keys -H: hex
- send-prefix: send prefix key

#### test_tmux_options_and_settings

- set-option -g: global
- set-option -a: append
- set-option: mouse on
- set-option -s: server option
- set-window-option: monitor activity
- set-window-option -g: global
- show-options -g: global options
- show-options -s: server options
- show-window-options: window options
- show-window-options -g: global window options

#### test_tmux_environment_variables

- set-environment -g: global env
- set-environment: session env
- set-environment -gur: update then remove
- show-environment -g: global env
- show-environment: session env

#### test_tmux_hooks

- set-hook: session-created
- set-hook: client-attached
- show-hooks -g: global hooks
- set-hook -gu: remove global hook
- set-hook -gu: remove hook

#### test_tmux_messages_and_display

- display-message: show message
- display-message -p: print format
- show-messages: message log
- display-popup -C: close popup
- clear-history: clear pane history

#### test_tmux_conditional_and_shell_execution

- if-shell: true condition
- run-shell: run shell command
- run-shell -b: background
- command-prompt: open prompt
- confirm-before: confirm dialog

#### test_tmux_source_and_configuration

- source-file: source config

#### test_tmux_copy_mode

- copy-mode: enter copy mode

#### test_tmux_find_window

- find-window: search windows

#### test_tmux_choose_commands_interactive

- choose-tree -G: tree display
- choose-client: client selection

#### test_tmux_clock_mode

- clock-mode: show clock

#### test_tmux_lock_management

- lock-server: lock server
- lock-session: lock session

#### test_tmux_show_prompt_history

- show-prompt-history: prompt history
- clear-prompt-history: clear prompt history

#### test_tmux_waitfor_event_channels

- wait-for -L: lock channel

#### test_tmux_cleanup_kill_sessions

- kill-session: kill renamed_sess
- kill-session: kill sess_fmt
- kill-session: kill sess_sz
- kill-session: kill sess_flags
- kill-session: kill sess_env
- kill-session: kill main test session
- kill-server: terminate server

#### test_tmux_error_handling

- Error: nonexistent session
- Error: invalid option

</details>

---

## tzdata

<details>
<summary><b>tzdata — 1 个用例 / 3 个功能点</b></summary>

#### test_tzdata_main

- 获取 tzselect 版本信息
- 获取 zdump 版本信息
- 获取 zic 版本信息

</details>

---

## uid_wrapper

<details>
<summary><b>uid_wrapper — 1 个用例 / 4 个功能点</b></summary>

#### test_uid_wrapper_main

- 获取 uid_wrapper 版本信息
- 列出 uid_wrapper 文件列表
- 检查共享库文件
- 检查头文件和 pkg-config 文件

</details>

---

## unbound

<details>
<summary><b>unbound — 1 个用例 / 5 个功能点</b></summary>

#### test_unbound_main

- 获取 unbound 版本信息
- 列出包内二进制文件
- 检查 systemd 服务文件
- 检查配置文件
- 检查手册页

</details>

---

## unzip

<details>
<summary><b>unzip — 1 个用例 / 4 个功能点</b></summary>

#### test_unzip_main

- 获取 unzip 版本信息
- 获取 funzip 版本信息
- 获取 zipgrep 版本信息
- 获取 zipinfo 版本信息

</details>

---

## util-linux

<details>
<summary><b>util-linux — 2 个用例 / 31 个功能点</b></summary>

#### test_util_linux_version_help

- addpart 版本信息
- addpart 帮助信息
- agetty 版本信息
- agetty 帮助信息
- blkid 版本信息
- blkid 帮助信息
- blkdiscard 版本信息
- blkdiscard 帮助信息
- blockdev 版本信息
- blockdev 帮助信息
- cal 版本信息
- cal 帮助信息
- cfdisk 版本信息
- cfdisk 帮助信息
- chcpu 版本信息
- chcpu 帮助信息
- chfn 版本信息
- chfn 帮助信息
- chmem 版本信息
- chmem 帮助信息
- choom 版本信息
- choom 帮助信息
- chrt 版本信息
- chrt 帮助信息
- bits 版本信息
- bits 帮助信息
- blkpr 版本信息
- blkpr 帮助信息
- blkzone 版本信息
- blkzone 帮助信息

#### test_util_linux_error_handling

- addpart: 无效选项

</details>

---

## vim

<details>
<summary><b>vim — 1 个用例 / 1 个功能点</b></summary>

#### test_vim_main

- 获取 vim 版本信息

</details>

---

## weston

<details>
<summary><b>weston — 9 个用例 / 9 个功能点</b></summary>

#### test_weston_version

- weston version

#### test_weston_help

- weston help

#### test_weston_weston_terminal_headless

- weston-terminal help

#### test_weston_weston_debug

- weston-debug help

#### test_weston_screenshooter

- weston-screenshooter help

#### test_weston_wcapdecode

- wcap-decode help

#### test_weston_backend_check

- Available backends

#### test_weston_headless_backend_test

- weston: headless backend

#### test_weston_error_handling

- weston: invalid option

</details>

---

## wget

<details>
<summary><b>wget — 15 个用例 / 18 个功能点</b></summary>

#### test_wget_basic_download

- Test downloading a small file

#### test_wget_output_options

- test_wget_output_options

#### test_wget_verbose_and_quiet_modes

- test_wget_verbose_and_quiet_modes

#### test_wget_spider_mode

- test_wget_spider_mode

#### test_wget_header_options

- test_wget_header_options

#### test_wget_user_agent

- test_wget_user_agent

#### test_wget_timeout_and_retries

- test_wget_timeout_and_retries

#### test_wget_recursive_download

- Test mirror mode (limited depth)

#### test_wget_continue_and_mirror

- Test continue option

#### test_wget_rate_limiting

- test_wget_rate_limiting

#### test_wget_progress_indicators

- test_wget_progress_indicators

#### test_wget_error_handling

- Invalid URL
- 404 error
- Invalid option

#### test_wget_directory_listing

- test_wget_directory_listing

#### test_wget_timestamps

- test_wget_timestamps

#### test_wget_special_features

- Follow redirects (default)
- Content disposition

</details>

---

## wget2

<details>
<summary><b>wget2 — 15 个用例 / 17 个功能点</b></summary>

#### test_wget2_basic_download

- test_wget2_basic_download

#### test_wget2_output_file_options

- test_wget2_output_file_options

#### test_wget2_verbose_modes

- test_wget2_verbose_modes

#### test_wget2_spider_mode

- test_wget2_spider_mode

#### test_wget2_headers

- test_wget2_headers

#### test_wget2_user_agent

- test_wget2_user_agent

#### test_wget2_timeouts_and_retries

- test_wget2_timeouts_and_retries

#### test_wget2_continue_download

- test_wget2_continue_download

#### test_wget2_rate_limiting

- test_wget2_rate_limiting

#### test_wget2_http2_support

- test_wget2_http2_support

#### test_wget2_tls_options

- test_wget2_tls_options

#### test_wget2_error_handling

- Invalid URL
- 404 error
- Invalid option

#### test_wget2_follow_redirects

- test_wget2_follow_redirects

#### test_wget2_content_disposition

- test_wget2_content_disposition

#### test_wget2_plugin_system

- test_wget2_plugin_system

</details>

---

## which

<details>
<summary><b>which — 1 个用例 / 1 个功能点</b></summary>

#### test_which_main

- 获取 which 版本信息

</details>

---

## xmlto

<details>
<summary><b>xmlto — 2 个用例 / 3 个功能点</b></summary>

#### test_xmlto_xmlto_basic

- 检查主要工具可执行性

#### test_xmlto_xmlto_version

- 获取 xmlto 帮助信息
- 获取 xmlto 版本信息

</details>

---

## xxhash

<details>
<summary><b>xxhash — 2 个用例 / 3 个功能点</b></summary>

#### test_xxhash_xxhash_basic

- 检查主要工具可执行性

#### test_xxhash_xxhash_version

- 获取 xxhash 帮助信息
- 获取 xxhash 版本信息

</details>

---

## xz

<details>
<summary><b>xz — 2 个用例 / 31 个功能点</b></summary>

#### test_xz_version_help

- xz 版本信息
- xz 帮助信息
- unxz 版本信息
- unxz 帮助信息
- xzcat 版本信息
- xzcat 帮助信息
- lzma 版本信息
- lzma 帮助信息
- unlzma 版本信息
- unlzma 帮助信息
- lzcat 版本信息
- lzcat 帮助信息
- lzcmp 版本信息
- lzcmp 帮助信息
- lzdiff 版本信息
- lzdiff 帮助信息
- lzgrep 版本信息
- lzgrep 帮助信息
- lzless 版本信息
- lzless 帮助信息
- lzmore 版本信息
- lzmore 帮助信息
- lzmadec 版本信息
- lzmadec 帮助信息
- lzmainfo 版本信息
- lzmainfo 帮助信息
- lzegrep 版本信息
- lzegrep 帮助信息
- lzfgrep 版本信息
- lzfgrep 帮助信息

#### test_xz_error_handling

- xz: 无效选项

</details>

---

## zstd

<details>
<summary><b>zstd — 2 个用例 / 13 个功能点</b></summary>

#### test_zstd_version_help

- zstd 版本信息
- zstd 帮助信息
- unzstd 版本信息
- unzstd 帮助信息
- zstdcat 版本信息
- zstdcat 帮助信息
- zstdgrep 版本信息
- zstdgrep 帮助信息
- zstdless 版本信息
- zstdless 帮助信息
- zstdmt 版本信息
- zstdmt 帮助信息

#### test_zstd_error_handling

- zstd: 无效选项

</details>
