# make 功能测试覆盖详情

共 **9** 个测试套，**21** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_make_basic_makefile_execution | 4 cases | Run default target |
| | | Run specific target |
| | | Run clean target |
| | | make -s: silent mode |
| test_make_variables | 2 cases | Variable expansion |
| | | Override variable |
| test_make_options | 7 cases | make -n: dry run |
| | | make -B: always make |
| | | make --just-print |
| | | make -d: debug output |
| | | make --debug=b: basic debug |
| | | make -q: question mode |
| | | make -s: silent |
| test_make_parallel_execution | 1 cases | make -j2: parallel 2 jobs |
| test_make_environment | 2 cases | make -e: environment overrides |
| | | Environment variable in make |
| test_make_directory_change | 1 cases | make -C: change directory |
| test_make_include | 1 cases | Include file |
| test_make_gmake_alias | 1 cases | gmake is GNU Make |
| test_make_error_handling | 2 cases | make -k: continue on error |
| | | make -i: ignore errors |
