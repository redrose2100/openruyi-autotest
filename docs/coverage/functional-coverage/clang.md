# clang 功能测试覆盖详情

共 **15** 个测试用例，**25** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| clang | test_clang_basic_c_compilation | Compile hello.c |
| | | Run compiled binary |
| | | Output is ELF binary |
| clang | test_clang_basic_c_compilation | Compile C++ from hello.c |
| | | Run C++ binary |
| clang | test_clang_compileonly | clang -c: compile only |
| | | Object file exists |
| clang | test_clang_optimization_levels | Optimization -$lvl |
| clang | test_clang_debug_and_warnings | Debug symbols |
| | | -Wall warnings |
| | | -Wextra warnings |
| | | -Werror |
| clang | test_clang_c_standards | C standard: $std |
| clang | test_clang_c_standards | C++ standard: $std |
| clang | test_clang_preprocessor | clang -E: preprocess |
| | | clang -dM: dump macros |
| clang | test_clang_static_analysis | clang --analyze: static analysis |
| clang | test_clang_clangcl_msvc_compat | clang-cl help |
| clang | test_clang_clangcpp | clang-cpp: preprocessor |
| clang | test_clang_clangscandeps | clang-scan-deps help |
| clang | test_clang_linking_options | Compile with -fPIC |
| | | clang -shared: shared library |
| clang | test_clang_verbose_mode | clang -v: verbose |
| clang | test_clang_error_handling | Compilation error |
| | | Invalid option |
