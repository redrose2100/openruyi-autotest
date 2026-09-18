# cloud-utils-growpart 功能测试覆盖详情

共 **6** 个测试套，**10** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_cloud_utils_growpart_help_and_version | 2 cases | growpart help |
| | | growpart -h: short help |
| test_cloud_utils_growpart_diskpartition_info | 2 cases | lsblk: list block devices |
| | | df: disk free space |
| test_cloud_utils_growpart_dryrun_no_actual_resize | 1 cases | growpart -N: dry run |
| test_cloud_utils_growpart_free_percent_option | 1 cases | growpart: has free-percent option |
| test_cloud_utils_growpart_fudge_factor_option | 1 cases | growpart: has fudge option |
| test_cloud_utils_growpart_error_handling | 3 cases | growpart: no args (expected fail) |
| | | growpart: nonexistent disk |
| | | growpart: invalid option |
