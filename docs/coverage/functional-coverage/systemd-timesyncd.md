# systemd-timesyncd 功能测试覆盖详情

共 **5** 个测试套，**13** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_systemd_timesyncd_service_status | 4 cases | Service status |
| | | Time sync status |
| | | Timesync detail |
| | | Is enabled |
| test_systemd_timesyncd_ntp_management | 4 cases | Fallback NTP servers |
| | | Current NTP server |
| | | Server address |
| | | NTP servers list |
| test_systemd_timesyncd_service_control | 2 cases | Restart service |
| | | Is active |
| test_systemd_timesyncd_configuration | 2 cases | Config file |
| | | Cat config |
| test_systemd_timesyncd_systemdtimewaitsync | 1 cases | Wait sync service |
