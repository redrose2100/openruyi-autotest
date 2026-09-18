# iputils 功能测试覆盖详情

共 **10** 个测试用例，**33** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| iputils | test_iputils_ping_basic_functionality | Ping localhost |
| | | Ping with count limit |
| | | Ping with interval |
| | | Ping with packet size |
| | | Ping with timeout |
| iputils | test_iputils_ping_advanced_options | Ping with flood mode (requires root) |
| | | Ping with numeric output |
| | | Ping with quiet mode |
| | | Ping with verbose output |
| | | Ping with timestamp |
| iputils | test_iputils_ping6_ipv6 | Ping6 localhost |
| | | Ping6 with count |
| iputils | test_iputils_traceroute6 | Basic traceroute6 to localhost |
| | | traceroute6 with max hops |
| | | traceroute6 with wait time |
| iputils | test_iputils_tracepath | Basic tracepath to localhost |
| | | tracepath with max hops |
| | | tracepath IPv6 |
| iputils | test_iputils_arping | ARP ping to localhost interface |
| | | arping with count |
| | | arping with timeout |
| iputils | test_iputils_clockdiff | Clock difference to localhost |
| | | clockdiff with IPv6 |
| iputils | test_iputils_ping_error_handling | Ping unreachable address |
| | | Ping with invalid address |
| | | Ping with invalid count |
| | | Ping with negative count |
| iputils | test_iputils_ping_special_scenarios | Ping broadcast address (may require special permissions) |
| | | Ping with source address |
| | | Ping with TTL |
| | | Continuous ping (limited by timeout) |
| iputils | test_iputils_network_interface_testing | Ping via specific interface |
| | | Multiple ping instances |
