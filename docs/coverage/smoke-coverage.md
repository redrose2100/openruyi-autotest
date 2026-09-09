# 冒烟测试覆盖详情

> 最后更新: 2026-06-15 | 自动生成
> 测试环境: openRuyi (10.20.237.192:12055)
> 验证结果: **100/100 通过** ✅

共 **17** 个类别，**100** 个测试用例

## 全部类别一览

| 类别 | 用例数 | 主要工具 | 说明 |
|------|:---:|------|------|
| [archive](#archive) | 5 | gzip, tar, xz | 文件压缩归档 |
| [dev_tools](#devtools) | 4 | gcc, make, ldd, python3 | 开发编译工具 |
| [disk_fs](#diskfs) | 4 | lsblk, mount, fstab | 磁盘文件系统 |
| [filesystem](#filesystem) | 10 | cat, cp, mv, rm, ls, touch, ln, mkdir, stat, file | 文件系统基本操作 |
| [kernel](#kernel) | 5 | uname, lsmod, modprobe, sysctl | 内核模块参数 |
| [logging](#logging) | 5 | dmesg, last, logrotate, logger, journalctl | 系统日志管理 |
| [network](#network) | 8 | ip, ping, curl, wget, ssh, ss, hostname | 网络配置诊断 |
| [package_mgmt](#packagemgmt) | 5 | rpm, dnf | 软件包管理 |
| [permissions](#permissions) | 4 | chmod, chown, sticky bit | 文件权限管理 |
| [process](#process) | 5 | ps, kill, pidof, pgrep, nproc | 进程管理 |
| [scripting](#scripting) | 5 | printf, env, sleep, tee, shebang | 脚本工具 |
| [security](#security) | 4 | sudo, ulimit, umask | 安全资源限制 |
| [service_mgmt](#servicemgmt) | 5 | systemctl, journalctl, hostnamectl, timedatectl, systemd-analyze | 系统服务管理 |
| [shell_basics](#shellbasics) | 8 | bash, test, pipe, redirect, glob, loops, variables | Shell 基础 |
| [system_info](#systeminfo) | 8 | uname, df, du, free, hostname, uptime, date | 系统信息查询 |
| [text_processing](#textprocessing) | 10 | grep, awk, sed, cut, sort, uniq, diff, find, tr, wc, head, tail | 文本处理 |
| [user_mgmt](#usermgmt) | 5 | whoami, id, groups, passwd, sudo, /etc/skel | 用户组管理 |

---

## archive

<details open><summary>5 个测试用例</summary>

- `test_smoke_gzip_compress` — gzip 压缩 / gunzip 解压
- `test_smoke_tar_archive` — tar -cf 创建 / -tf 列出 / -xf 解压
- `test_smoke_tar_gz_create` — tar -czf 创建 .tar.gz / -xzf 解压
- `test_smoke_tar_xz_create` — tar -cJf 创建 .tar.xz
- `test_smoke_xz_compress` — xz 压缩 / unxz 解压

</details>

## dev_tools

<details open><summary>4 个测试用例</summary>

- `test_smoke_gcc_compile` — gcc 编译 C 程序并执行
- `test_smoke_ldd_deps` — ldd 查看二进制动态库依赖
- `test_smoke_make_build` — make 构建 C 项目
- `test_smoke_python_interpreter` — python3 解释器基本执行

</details>

## disk_fs

<details open><summary>4 个测试用例</summary>

- `test_smoke_fstab_check` — /etc/fstab 文件系统表验证
- `test_smoke_lsblk_block_devices` — lsblk 列出块设备 / lsblk -f 文件系统信息
- `test_smoke_mount_list` — mount 查看已挂载文件系统
- `test_smoke_proc_partitions` — /proc/partitions / /proc/filesystems 内核分区信息

</details>

## filesystem

<details open><summary>10 个测试用例</summary>

- `test_smoke_cat_read_file` — cat 读取文件内容
- `test_smoke_cp_copy_file` — cp 复制文件与目录 / diff 验证一致性
- `test_smoke_file_type_detect` — file 检测文件类型（文本/二进制/目录）
- `test_smoke_ln_hardlink_symlink` — ln 硬链接 / ln -s 符号链接
- `test_smoke_ls_list_files` — ls 列出文件 / ls -la 详细列表 / ls -d 目录
- `test_smoke_mkdir_rmdir_directory` — mkdir 创建目录 / mkdir -p 嵌套创建 / rmdir 删除
- `test_smoke_mv_move_file` — mv 重命名 / 移动文件
- `test_smoke_rm_delete_file` — rm 删除文件 / rm -rf 删除目录
- `test_smoke_stat_file_info` — stat 查看文件详细信息 / stat -c 格式化输出
- `test_smoke_touch_create_file` — touch 创建空文件 / touch -t 设置时间戳

</details>

## kernel

<details open><summary>5 个测试用例</summary>

- `test_smoke_kernel_version_verify` — uname -r 内核版本 / /proc/cmdline 启动参数 / /proc/version
- `test_smoke_lsmod_modules` — lsmod 列出已加载内核模块
- `test_smoke_modprobe_check` — modprobe 模块管理 / /lib/modules 模块目录
- `test_smoke_proc_sys_check` — /proc/sys 内核参数目录
- `test_smoke_sysctl_kernel_params` — sysctl -a 列出内核参数 / sysctl 读取特定参数

</details>

## logging

<details open><summary>5 个测试用例</summary>

- `test_smoke_dmesg_kernel_log` — dmesg 查看内核启动日志
- `test_smoke_last_login_records` — last 查看登录记录 / /var/log/wtmp
- `test_smoke_logrotate_config` — logrotate 日志轮转配置 / /etc/logrotate.d
- `test_smoke_syslog_available` — logger 写入系统日志 / journalctl 查询
- `test_smoke_var_log_check` — /var/log 目录及日志文件完整性

</details>

## network

<details open><summary>8 个测试用例</summary>

- `test_smoke_curl_http` — curl 获取 HTTP 内容
- `test_smoke_hostname_resolve` — hostname 主机名解析
- `test_smoke_ip_network_config` — ip addr / ip link 网络接口配置
- `test_smoke_loopback_interface` — lo 回环接口 ping 127.0.0.1
- `test_smoke_ping_localhost` — ping localhost 连通性
- `test_smoke_ss_socket_stats` — ss 查看 socket 连接状态
- `test_smoke_ssh_client_check` — ssh 客户端可用性检查
- `test_smoke_wget_download` — wget 文件下载

</details>

## package_mgmt

<details open><summary>5 个测试用例</summary>

- `test_smoke_dnf_package_manager` — dnf 包管理器基本功能
- `test_smoke_os_release_check` — /etc/os-release 系统版本信息
- `test_smoke_rpm_query` — rpm -qa 查询已安装包
- `test_smoke_rpm_scripts` — rpm 脚本相关功能
- `test_smoke_rpm_verify` — rpm -V 验证包完整性

</details>

## permissions

<details open><summary>4 个测试用例</summary>

- `test_smoke_chmod_recursive` — chmod 递归修改权限 / chmod 数字模式
- `test_smoke_chown_ownership` — chown 修改文件所有者
- `test_smoke_special_perms` — SUID / SGID / sticky 特殊权限
- `test_smoke_sticky_bit_tmp` — /tmp 目录 sticky bit 验证

</details>

## process

<details open><summary>5 个测试用例</summary>

- `test_smoke_jobs_background` — & 后台任务 / fg 前台 / jobs 任务列表
- `test_smoke_kill_signal` — kill 发送信号 / kill -l 信号列表
- `test_smoke_nproc_cpu_count` — nproc 查看 CPU 核心数
- `test_smoke_pidof_pgrep` — pidof / pgrep 按名称查找进程
- `test_smoke_ps_process_list` — ps aux 列出进程 / ps -ef 完整格式

</details>

## scripting

<details open><summary>5 个测试用例</summary>

- `test_smoke_env_variables` — env 查看环境变量 / export 设置变量
- `test_smoke_printf_format` — printf 格式化输出
- `test_smoke_shebang_script` — #!/bin/sh 脚本执行
- `test_smoke_sleep_timeout` — sleep 延时 / timeout 超时控制
- `test_smoke_tee_write` — tee 同时输出到文件和 stdout

</details>

## security

<details open><summary>4 个测试用例</summary>

- `test_smoke_file_permissions` — 文件默认权限检查（644/755）
- `test_smoke_sudo_access` — sudo 权限验证
- `test_smoke_ulimit_resources` — ulimit -a 资源限制查看
- `test_smoke_umask_default` — umask 默认掩码值

</details>

## service_mgmt

<details open><summary>5 个测试用例</summary>

- `test_smoke_hostnamectl` — hostnamectl 主机名管理
- `test_smoke_journalctl_logs` — journalctl 查看系统日志
- `test_smoke_systemctl_status` — systemctl status 服务状态
- `test_smoke_systemd_analyze` — systemd-analyze 启动时间分析 / systemd-analyze blame
- `test_smoke_timedatectl_time` — timedatectl 时间日期管理

</details>

## shell_basics

<details open><summary>8 个测试用例</summary>

- `test_smoke_bash_version` — bash --version 版本查看
- `test_smoke_exit_code_handling` — $? 退出码 / && || 条件执行
- `test_smoke_for_while_loops` — for 循环 / while 循环
- `test_smoke_globbing_wildcard` — * 通配符 / ? 单字符匹配
- `test_smoke_if_condition_test` — if / test / [ ] 条件判断
- `test_smoke_pipe_redirect` — | 管道 / > >> 重定向 / < 输入重定向
- `test_smoke_subshell_command` — $( ) 命令替换 / ` ` 反引号
- `test_smoke_variable_expansion` — $变量 / ${变量} 变量展开

</details>

## system_info

<details open><summary>8 个测试用例</summary>

- `test_smoke_cpu_mem_info` — /proc/cpuinfo / /proc/meminfo CPU 和内存信息
- `test_smoke_date_time` — date 日期时间显示
- `test_smoke_df_disk_usage` — df -h 磁盘空间使用
- `test_smoke_du_disk_usage` — du -sh 目录磁盘占用
- `test_smoke_free_memory` — free -h 内存使用情况
- `test_smoke_hostname_check` — hostname 主机名查询
- `test_smoke_uname_system_info` — uname -a 系统完整信息
- `test_smoke_uptime_load` — uptime 系统运行时间和负载

</details>

## text_processing

<details open><summary>10 个测试用例</summary>

- `test_smoke_awk_text_processing` — awk 文本处理（字段提取/条件过滤）
- `test_smoke_cut_field_extract` — cut -d -f 按分隔符提取字段
- `test_smoke_diff_compare` — diff 文件差异比较
- `test_smoke_find_search_files` — find 按名称/类型搜索文件
- `test_smoke_grep_search` — grep 文本搜索 / grep -v 反向 / grep -i 忽略大小写
- `test_smoke_head_tail_lines` — head 前 N 行 / tail 后 N 行
- `test_smoke_sed_substitution` — sed 文本替换
- `test_smoke_sort_uniq_dedup` — sort 排序 / uniq 去重
- `test_smoke_tr_translate` — tr 字符转换
- `test_smoke_wc_count` — wc -l -w -c 行数/词数/字符数统计

</details>

## user_mgmt

<details open><summary>5 个测试用例</summary>

- `test_smoke_etc_skel_home` — /etc/skel 用户骨架目录
- `test_smoke_groups_membership` — groups 查看用户组 / /etc/group
- `test_smoke_passwd_shadow` — /etc/passwd / /etc/shadow 用户账户文件
- `test_smoke_sudo_check` — sudo 配置检查
- `test_smoke_whoami_id` — whoami 当前用户 / id 用户 UID/GID

</details>
