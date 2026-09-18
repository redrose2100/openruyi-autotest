# procps-ng 功能测试覆盖详情

共 **14** 个测试用例，**53** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| procps-ng | test_procps_ng_ps_command_basic_functionality | Basic ps output |
| | | ps with full format |
| | | ps with custom format |
| | | ps showing all processes |
| | | ps with tree view |
| procps-ng | test_procps_ng_ps_command_advanced_features | Filter by user |
| | | Filter by PID |
| | | Show threads |
| | | Process hierarchy |
| | | Sort by CPU usage |
| | | Sort by memory usage |
| procps-ng | test_procps_ng_free_command | Basic memory info |
| | | Human-readable format |
| | | Display in different units |
| | | Continuous monitoring (single iteration) |
| | | Show total column |
| | | Show low/high memory |
| procps-ng | test_procps_ng_top_command | Basic top (batch mode, single iteration) |
| | | Top with specific number of processes |
| | | Top sorted by memory |
| | | Top with delay |
| procps-ng | test_procps_ng_vmstat_command | Basic vmstat output |
| | | vmstat with custom intervals |
| | | vmstat with slabs info |
| | | vmstat with disk stats |
| | | vmstat with partitions |
| procps-ng | test_procps_ng_uptime_and_w_commands | System uptime |
| | | Show users |
| | | Show who is logged in |
| procps-ng | test_procps_ng_kill_command | Start a background process |
| | | List signal numbers |
| | | Send SIGTERM |
| | | Wait for process to terminate |
| | | Verify process terminated |
| procps-ng | test_procps_ng_pidof_and_pgrep | Find PID by name |
| | | pgrep basic usage |
| | | pgrep with full command line |
| procps-ng | test_procps_ng_pwdx_and_pmap | Show process working directory |
| | | Show process memory map |
| procps-ng | test_procps_ng_sysctl_if_available | List all sysctl parameters |
| | | Read specific parameter |
| procps-ng | test_procps_ng_error_handling | ps with invalid PID |
| | | kill with invalid PID |
| | | free with invalid option |
| procps-ng | test_procps_ng_special_scenarios | ps with environment variables |
| | | Process with real-time priority |
| | | Show process namespaces |
| procps-ng | test_procps_ng_pkill_and_pidwait | pkill version check |
| | | pidwait version check |
| procps-ng | test_procps_ng_slabtop_tload_watch_hugetop | slabtop display |
| | | tload version |
| | | watch basic usage |
| | | hugetop |
