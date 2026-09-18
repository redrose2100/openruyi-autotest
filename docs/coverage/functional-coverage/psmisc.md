# psmisc 功能测试覆盖详情

共 **13** 个测试套，**22** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_psmisc_fuser_basic | 1 cases | Test fuser on /tmp |
| test_psmisc_fuser_with_processes | 1 cases | Show processes using /tmp |
| test_psmisc_fuser_mount_points | 1 cases | test_psmisc_fuser_mount_points |
| test_psmisc_fuser_with_options | 1 cases | test_psmisc_fuser_with_options |
| test_psmisc_pstree_basic | 1 cases | test_psmisc_pstree_basic |
| test_psmisc_pstree_with_options | 6 cases | Show PIDs |
| | | Show numeric sort |
| | | Compact tree |
| | | Highlight current process |
| | | Show full details |
| | | Show only one user's processes |
| test_psmisc_killall_basic | 3 cases | Start test process |
| | | Try killall (may not kill itself) |
| | | Clean up |
| test_psmisc_prtstat | 1 cases | test_psmisc_prtstat |
| test_psmisc_peekfd | 1 cases | test_psmisc_peekfd |
| test_psmisc_pslog | 1 cases | test_psmisc_pslog |
| test_psmisc_killall_with_signals | 2 cases | List signal names |
| | | Test signal send |
| test_psmisc_fuser_special_cases | 2 cases | fuser on unix socket |
| | | fuser reset signal output |
| test_psmisc_error_handling | 1 cases | test_psmisc_error_handling |
