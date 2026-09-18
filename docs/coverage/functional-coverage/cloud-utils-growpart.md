# cloud-utils-growpart 功能测试覆盖详情

共 **6** 个测试用例，**10** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| cloud-utils-growpart | test_cloud_utils_growpart_help_and_version | growpart help |
| | | growpart -h: short help |
| cloud-utils-growpart | test_cloud_utils_growpart_diskpartition_info | lsblk: list block devices |
| | | df: disk free space |
| cloud-utils-growpart | test_cloud_utils_growpart_dryrun_no_actual_resize | growpart -N: dry run |
| cloud-utils-growpart | test_cloud_utils_growpart_free_percent_option | growpart: has free-percent option |
| cloud-utils-growpart | test_cloud_utils_growpart_fudge_factor_option | growpart: has fudge option |
| cloud-utils-growpart | test_cloud_utils_growpart_error_handling | growpart: no args (expected fail) |
| | | growpart: nonexistent disk |
| | | growpart: invalid option |
