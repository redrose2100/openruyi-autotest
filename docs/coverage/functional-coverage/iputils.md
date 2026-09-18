# iputils 功能测试覆盖详情

共 **10** 个测试套，**33** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_iputils_ping_basic_functionality | 5 cases | Ping localhost |
| | | Ping with count limit |
| | | Ping with interval |
| | | Ping with packet size |
| | | Ping with timeout |
| test_iputils_ping_advanced_options | 5 cases | Ping with flood mode (requires root) |
| | | Ping with numeric output |
| | | Ping with quiet mode |
| | | Ping with verbose output |
| | | Ping with timestamp |
| test_iputils_ping6_ipv6 | 2 cases | Ping6 localhost |
| | | Ping6 with count |
| test_iputils_traceroute6 | 3 cases | Basic traceroute6 to localhost |
| | | traceroute6 with max hops |
| | | traceroute6 with wait time |
| test_iputils_tracepath | 3 cases | Basic tracepath to localhost |
| | | tracepath with max hops |
| | | tracepath IPv6 |
| test_iputils_arping | 3 cases | ARP ping to localhost interface |
| | | arping with count |
| | | arping with timeout |
| test_iputils_clockdiff | 2 cases | Clock difference to localhost |
| | | clockdiff with IPv6 |
| test_iputils_ping_error_handling | 4 cases | Ping unreachable address |
| | | Ping with invalid address |
| | | Ping with invalid count |
| | | Ping with negative count |
| test_iputils_ping_special_scenarios | 4 cases | Ping broadcast address (may require special permissions) |
| | | Ping with source address |
| | | Ping with TTL |
| | | Continuous ping (limited by timeout) |
| test_iputils_network_interface_testing | 2 cases | Ping via specific interface |
| | | Multiple ping instances |
