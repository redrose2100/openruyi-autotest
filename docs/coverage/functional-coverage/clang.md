# clang 功能测试覆盖详情

共 **15** 个测试套，**25** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_clang_basic_c_compilation | 3 cases | Compile hello.c |
| | | Run compiled binary |
| | | Output is ELF binary |
| test_clang_basic_c_compilation | 2 cases | Compile C++ from hello.c |
| | | Run C++ binary |
| test_clang_compileonly | 2 cases | clang -c: compile only |
| | | Object file exists |
| test_clang_optimization_levels | 1 cases | Optimization -$lvl |
| test_clang_debug_and_warnings | 4 cases | Debug symbols |
| | | -Wall warnings |
| | | -Wextra warnings |
| | | -Werror |
| test_clang_c_standards | 1 cases | C standard: $std |
| test_clang_c_standards | 1 cases | C++ standard: $std |
| test_clang_preprocessor | 2 cases | clang -E: preprocess |
| | | clang -dM: dump macros |
| test_clang_static_analysis | 1 cases | clang --analyze: static analysis |
| test_clang_clangcl_msvc_compat | 1 cases | clang-cl help |
| test_clang_clangcpp | 1 cases | clang-cpp: preprocessor |
| test_clang_clangscandeps | 1 cases | clang-scan-deps help |
| test_clang_linking_options | 2 cases | Compile with -fPIC |
| | | clang -shared: shared library |
| test_clang_verbose_mode | 1 cases | clang -v: verbose |
| test_clang_error_handling | 2 cases | Compilation error |
| | | Invalid option |
