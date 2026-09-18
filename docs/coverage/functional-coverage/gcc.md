# gcc 功能测试覆盖详情

共 **12** 个测试用例，**52** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| gcc | test_gcc_basic_c_compilation | Compile hello.c to hello |
| | | Run compiled hello |
| | | Verify output is ELF binary |
| | | Compile with -o flag |
| | | Run myhello |
| gcc | test_gcc_c_compilation | Compile hello.cpp |
| | | Compile with C++11 standard |
| gcc | test_gcc_compiler_optimization_flags | Compile with -O0 |
| | | Compile with -O2 |
| | | Compile with debug symbols -g |
| | | Verify debug symbols present |
| gcc | test_gcc_preprocessor | Preprocess with -E |
| | | Verify macro expanded in preprocessed output |
| | | Compile preprocessed .i file |
| | | Run from preprocessed source |
| | | Compile with -D flag |
| | | Run with -D defined macro |
| gcc | test_gcc_assembly_output | Generate assembly with -S |
| | | Check main label in assembly |
| | | Assemble to object file |
| gcc | test_gcc_linking_and_libraries | Link with -lm |
| | | Run math linked program |
| | | Compile static binary |
| gcc | test_gcc_warning_flags | Compile with -Wall warnings enabled |
| | | Compile with -Werror |
| | | Compile with -pedantic |
| gcc | test_gcc_multifile_compilation | Compile add.c to object |
| | | Compile main.c to object |
| | | Link multiple objects |
| | | Run multi-file program |
| | | Compile multiple files in one command |
| | | Run single-command multi-file program |
| gcc | test_gcc_code_coverage_gcov | Compile with coverage flags |
| | | Run coverage test program |
| | | Run gcov |
| | | Check gcov output file exists |
| gcc | test_gcc_error_handling | Test type mismatch warning |
| gcc | test_gcc_special_features | Compile with C99 standard |
| | | Compile with __attribute__ |
| | | Run attribute test |
| | | Compile with -I include path |
| | | Run include path test |
| gcc | test_gcc_gcc_toolchain_utilities | gcc-ar version check |
| | | gcc-nm version check |
| | | gcc-ranlib version check |
| | | gcov-dump version check |
| | | gcov-tool version check |
| | | lto-dump version check |
| | | cc version check |
| | | cc equals gcc |
| | | c++ version check |
| | | c++ equals g++ |
