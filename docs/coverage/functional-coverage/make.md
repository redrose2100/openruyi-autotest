# make 功能测试覆盖详情

共 **9** 个测试用例，**21** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| make | test_make_basic_makefile_execution | Run default target |
| | | Run specific target |
| | | Run clean target |
| | | make -s: silent mode |
| make | test_make_variables | Variable expansion |
| | | Override variable |
| make | test_make_options | make -n: dry run |
| | | make -B: always make |
| | | make --just-print |
| | | make -d: debug output |
| | | make --debug=b: basic debug |
| | | make -q: question mode |
| | | make -s: silent |
| make | test_make_parallel_execution | make -j2: parallel 2 jobs |
| make | test_make_environment | make -e: environment overrides |
| | | Environment variable in make |
| make | test_make_directory_change | make -C: change directory |
| make | test_make_include | Include file |
| make | test_make_gmake_alias | gmake is GNU Make |
| make | test_make_error_handling | make -k: continue on error |
| | | make -i: ignore errors |
