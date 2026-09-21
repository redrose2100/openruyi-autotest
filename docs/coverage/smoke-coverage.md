# Smoke Test Coverage Details

> Last updated: 2026-06-15 | Auto-generated
> Test environment: openRuyi (10.20.237.192:12055)
> Verification result: **100/100 passed** ✅

**17** categories in total, **100** test cases

## All Categories Overview

| Category | Cases | Main Tools | Description |
|------|:---:|------|------|
| [archive](#archive) | 5 | gzip, tar, xz | File compression/archiving |
| [dev_tools](#devtools) | 4 | gcc, make, ldd, python3 | Development/build tools |
| [disk_fs](#diskfs) | 4 | lsblk, mount, fstab | Disk and filesystem |
| [filesystem](#filesystem) | 10 | cat, cp, mv, rm, ls, touch, ln, mkdir, stat, file | Basic filesystem operations |
| [kernel](#kernel) | 5 | uname, lsmod, modprobe, sysctl | Kernel modules/parameters |
| [logging](#logging) | 5 | dmesg, last, logrotate, logger, journalctl | System log management |
| [network](#network) | 8 | ip, ping, curl, wget, ssh, ss, hostname | Network config/diagnostics |
| [package_mgmt](#packagemgmt) | 5 | rpm, dnf | Package management |
| [permissions](#permissions) | 4 | chmod, chown, sticky bit | File permission management |
| [process](#process) | 5 | ps, kill, pidof, pgrep, nproc | Process management |
| [scripting](#scripting) | 5 | printf, env, sleep, tee, shebang | Scripting tools |
| [security](#security) | 4 | sudo, ulimit, umask | Security/resource limits |
| [service_mgmt](#servicemgmt) | 5 | systemctl, journalctl, hostnamectl, timedatectl, systemd-analyze | System service management |
| [shell_basics](#shellbasics) | 8 | bash, test, pipe, redirect, glob, loops, variables | Shell basics |
| [system_info](#systeminfo) | 8 | uname, df, du, free, hostname, uptime, date | System info query |
| [text_processing](#textprocessing) | 10 | grep, awk, sed, cut, sort, uniq, diff, find, tr, wc, head, tail | Text processing |
| [user_mgmt](#usermgmt) | 5 | whoami, id, groups, passwd, sudo, /etc/skel | User/group management |

---

## archive

<details open><summary>5 test cases</summary>

- `test_smoke_gzip_compress` — gzip compress / gunzip decompress
- `test_smoke_tar_archive` — tar -cf create / -tf list / -xf extract
- `test_smoke_tar_gz_create` — tar -czf create .tar.gz / -xzf extract
- `test_smoke_tar_xz_create` — tar -cJf create .tar.xz
- `test_smoke_xz_compress` — xz compress / unxz decompress

</details>

## dev_tools

<details open><summary>4 test cases</summary>

- `test_smoke_gcc_compile` — gcc compile C program and execute
- `test_smoke_ldd_deps` — ldd view binary dynamic library deps
- `test_smoke_make_build` — make build C project
- `test_smoke_python_interpreter` — python3 interpreter basic execution

</details>

## disk_fs

<details open><summary>4 test cases</summary>

- `test_smoke_fstab_check` — /etc/fstab filesystem table verification
- `test_smoke_lsblk_block_devices` — lsblk list block devices / lsblk -f filesystem info
- `test_smoke_mount_list` — mount view mounted filesystems
- `test_smoke_proc_partitions` — /proc/partitions / /proc/filesystems kernel partition info

</details>

## filesystem

<details open><summary>10 test cases</summary>

- `test_smoke_cat_read_file` — cat read file content
- `test_smoke_cp_copy_file` — cp copy files and dirs / diff verify consistency
- `test_smoke_file_type_detect` — file detect file type (text/binary/directory)
- `test_smoke_ln_hardlink_symlink` — ln hard link / ln -s symbolic link
- `test_smoke_ls_list_files` — ls list files / ls -la detailed list / ls -d directory
- `test_smoke_mkdir_rmdir_directory` — mkdir create dir / mkdir -p nested / rmdir remove
- `test_smoke_mv_move_file` — mv rename / move files
- `test_smoke_rm_delete_file` — rm delete file / rm -rf delete directory
- `test_smoke_stat_file_info` — stat view file details / stat -c formatted output
- `test_smoke_touch_create_file` — touch create empty file / touch -t set timestamp

</details>

## kernel

<details open><summary>5 test cases</summary>

- `test_smoke_kernel_version_verify` — uname -r kernel version / /proc/cmdline boot params / /proc/version
- `test_smoke_lsmod_modules` — lsmod list loaded kernel modules
- `test_smoke_modprobe_check` — modprobe module management / /lib/modules module dir
- `test_smoke_proc_sys_check` — /proc/sys kernel parameter directory
- `test_smoke_sysctl_kernel_params` — sysctl -a list kernel params / sysctl read specific param

</details>

## logging

<details open><summary>5 test cases</summary>

- `test_smoke_dmesg_kernel_log` — dmesg view kernel boot log
- `test_smoke_last_login_records` — last view login records / /var/log/wtmp
- `test_smoke_logrotate_config` — logrotate log rotation config / /etc/logrotate.d
- `test_smoke_syslog_available` — logger write to syslog / journalctl query
- `test_smoke_var_log_check` — /var/log directory and log file integrity

</details>

## network

<details open><summary>8 test cases</summary>

- `test_smoke_curl_http` — curl fetch HTTP content
- `test_smoke_hostname_resolve` — hostname resolution
- `test_smoke_ip_network_config` — ip addr / ip link network interface config
- `test_smoke_loopback_interface` — lo loopback interface ping 127.0.0.1
- `test_smoke_ping_localhost` — ping localhost connectivity
- `test_smoke_ss_socket_stats` — ss view socket connection status
- `test_smoke_ssh_client_check` — ssh client availability check
- `test_smoke_wget_download` — wget file download

</details>

## package_mgmt

<details open><summary>5 test cases</summary>

- `test_smoke_dnf_package_manager` — dnf package manager basic functions
- `test_smoke_os_release_check` — /etc/os-release system version info
- `test_smoke_rpm_query` — rpm -qa query installed packages
- `test_smoke_rpm_scripts` — rpm script-related features
- `test_smoke_rpm_verify` — rpm -V verify package integrity

</details>

## permissions

<details open><summary>4 test cases</summary>

- `test_smoke_chmod_recursive` — chmod recursive permission change / chmod numeric mode
- `test_smoke_chown_ownership` — chown change file owner
- `test_smoke_special_perms` — SUID / SGID / sticky special permissions
- `test_smoke_sticky_bit_tmp` — /tmp directory sticky bit verification

</details>

## process

<details open><summary>5 test cases</summary>

- `test_smoke_jobs_background` — & background task / fg foreground / jobs task list
- `test_smoke_kill_signal` — kill send signal / kill -l signal list
- `test_smoke_nproc_cpu_count` — nproc view CPU core count
- `test_smoke_pidof_pgrep` — pidof / pgrep find process by name
- `test_smoke_ps_process_list` — ps aux list processes / ps -ef full format

</details>

## scripting

<details open><summary>5 test cases</summary>

- `test_smoke_env_variables` — env view environment variables / export set variable
- `test_smoke_printf_format` — printf formatted output
- `test_smoke_shebang_script` — #!/bin/sh script execution
- `test_smoke_sleep_timeout` — sleep delay / timeout timeout control
- `test_smoke_tee_write` — tee write to both file and stdout

</details>

## security

<details open><summary>4 test cases</summary>

- `test_smoke_file_permissions` — file default permission check (644/755)
- `test_smoke_sudo_access` — sudo permission verification
- `test_smoke_ulimit_resources` — ulimit -a resource limits view
- `test_smoke_umask_default` — umask default mask value

</details>

## service_mgmt

<details open><summary>5 test cases</summary>

- `test_smoke_hostnamectl` — hostnamectl hostname management
- `test_smoke_journalctl_logs` — journalctl view system logs
- `test_smoke_systemctl_status` — systemctl status service status
- `test_smoke_systemd_analyze` — systemd-analyze boot time analysis / systemd-analyze blame
- `test_smoke_timedatectl_time` — timedatectl time/date management

</details>

## shell_basics

<details open><summary>8 test cases</summary>

- `test_smoke_bash_version` — bash --version version check
- `test_smoke_exit_code_handling` — $? exit code / && || conditional execution
- `test_smoke_for_while_loops` — for loop / while loop
- `test_smoke_globbing_wildcard` — * wildcard / ? single char match
- `test_smoke_if_condition_test` — if / test / [ ] condition evaluation
- `test_smoke_pipe_redirect` — | pipe / > >> redirect / < input redirect
- `test_smoke_subshell_command` — $( ) command substitution / backticks
- `test_smoke_variable_expansion` — $variable / ${variable} variable expansion

</details>

## system_info

<details open><summary>8 test cases</summary>

- `test_smoke_cpu_mem_info` — /proc/cpuinfo / /proc/meminfo CPU and memory info
- `test_smoke_date_time` — date date/time display
- `test_smoke_df_disk_usage` — df -h disk space usage
- `test_smoke_du_disk_usage` — du -sh directory disk usage
- `test_smoke_free_memory` — free -h memory usage
- `test_smoke_hostname_check` — hostname hostname query
- `test_smoke_uname_system_info` — uname -a complete system info
- `test_smoke_uptime_load` — uptime system uptime and load

</details>

## text_processing

<details open><summary>10 test cases</summary>

- `test_smoke_awk_text_processing` — awk text processing (field extraction/conditional filter)
- `test_smoke_cut_field_extract` — cut -d -f extract fields by delimiter
- `test_smoke_diff_compare` — diff file diff comparison
- `test_smoke_find_search_files` — find search files by name/type
- `test_smoke_grep_search` — grep text search / grep -v invert / grep -i case-insensitive
- `test_smoke_head_tail_lines` — head first N lines / tail last N lines
- `test_smoke_sed_substitution` — sed text substitution
- `test_smoke_sort_uniq_dedup` — sort ordering / uniq dedup
- `test_smoke_tr_translate` — tr character translation
- `test_smoke_wc_count` — wc -l -w -c line/word/char count

</details>

## user_mgmt

<details open><summary>5 test cases</summary>

- `test_smoke_etc_skel_home` — /etc/skel user skeleton directory
- `test_smoke_groups_membership` — groups view user groups / /etc/group
- `test_smoke_passwd_shadow` — /etc/passwd / /etc/shadow user account files
- `test_smoke_sudo_check` — sudo configuration check
- `test_smoke_whoami_id` — whoami current user / id user UID/GID

</details>
