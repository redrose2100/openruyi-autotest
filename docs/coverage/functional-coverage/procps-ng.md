# procps-ng 功能测试覆盖详情

共 **14** 个测试套，**53** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_procps_ng_ps_command_basic_functionality | 5 cases | Basic ps output |
| | | ps with full format |
| | | ps with custom format |
| | | ps showing all processes |
| | | ps with tree view |
| test_procps_ng_ps_command_advanced_features | 6 cases | Filter by user |
| | | Filter by PID |
| | | Show threads |
| | | Process hierarchy |
| | | Sort by CPU usage |
| | | Sort by memory usage |
| test_procps_ng_free_command | 6 cases | Basic memory info |
| | | Human-readable format |
| | | Display in different units |
| | | Continuous monitoring (single iteration) |
| | | Show total column |
| | | Show low/high memory |
| test_procps_ng_top_command | 4 cases | Basic top (batch mode, single iteration) |
| | | Top with specific number of processes |
| | | Top sorted by memory |
| | | Top with delay |
| test_procps_ng_vmstat_command | 5 cases | Basic vmstat output |
| | | vmstat with custom intervals |
| | | vmstat with slabs info |
| | | vmstat with disk stats |
| | | vmstat with partitions |
| test_procps_ng_uptime_and_w_commands | 3 cases | System uptime |
| | | Show users |
| | | Show who is logged in |
| test_procps_ng_kill_command | 5 cases | Start a background process |
| | | List signal numbers |
| | | Send SIGTERM |
| | | Wait for process to terminate |
| | | Verify process terminated |
| test_procps_ng_pidof_and_pgrep | 3 cases | Find PID by name |
| | | pgrep basic usage |
| | | pgrep with full command line |
| test_procps_ng_pwdx_and_pmap | 2 cases | Show process working directory |
| | | Show process memory map |
| test_procps_ng_sysctl_if_available | 2 cases | List all sysctl parameters |
| | | Read specific parameter |
| test_procps_ng_error_handling | 3 cases | ps with invalid PID |
| | | kill with invalid PID |
| | | free with invalid option |
| test_procps_ng_special_scenarios | 3 cases | ps with environment variables |
| | | Process with real-time priority |
| | | Show process namespaces |
| test_procps_ng_pkill_and_pidwait | 2 cases | pkill version check |
| | | pidwait version check |
| test_procps_ng_slabtop_tload_watch_hugetop | 4 cases | slabtop display |
| | | tload version |
| | | watch basic usage |
| | | hugetop |
