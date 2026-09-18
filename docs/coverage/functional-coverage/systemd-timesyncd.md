# systemd-timesyncd 功能测试覆盖详情

共 **5** 个测试用例，**13** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| systemd-timesyncd | test_systemd_timesyncd_service_status | Service status |
| | | Time sync status |
| | | Timesync detail |
| | | Is enabled |
| systemd-timesyncd | test_systemd_timesyncd_ntp_management | Fallback NTP servers |
| | | Current NTP server |
| | | Server address |
| | | NTP servers list |
| systemd-timesyncd | test_systemd_timesyncd_service_control | Restart service |
| | | Is active |
| systemd-timesyncd | test_systemd_timesyncd_configuration | Config file |
| | | Cat config |
| systemd-timesyncd | test_systemd_timesyncd_systemdtimewaitsync | Wait sync service |
