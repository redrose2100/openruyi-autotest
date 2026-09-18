# gcc 功能测试覆盖详情

共 **12** 个测试套，**52** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_gcc_basic_c_compilation | 5 cases | Compile hello.c to hello |
| | | Run compiled hello |
| | | Verify output is ELF binary |
| | | Compile with -o flag |
| | | Run myhello |
| test_gcc_c_compilation | 2 cases | Compile hello.cpp |
| | | Compile with C++11 standard |
| test_gcc_compiler_optimization_flags | 4 cases | Compile with -O0 |
| | | Compile with -O2 |
| | | Compile with debug symbols -g |
| | | Verify debug symbols present |
| test_gcc_preprocessor | 6 cases | Preprocess with -E |
| | | Verify macro expanded in preprocessed output |
| | | Compile preprocessed .i file |
| | | Run from preprocessed source |
| | | Compile with -D flag |
| | | Run with -D defined macro |
| test_gcc_assembly_output | 3 cases | Generate assembly with -S |
| | | Check main label in assembly |
| | | Assemble to object file |
| test_gcc_linking_and_libraries | 3 cases | Link with -lm |
| | | Run math linked program |
| | | Compile static binary |
| test_gcc_warning_flags | 3 cases | Compile with -Wall warnings enabled |
| | | Compile with -Werror |
| | | Compile with -pedantic |
| test_gcc_multifile_compilation | 6 cases | Compile add.c to object |
| | | Compile main.c to object |
| | | Link multiple objects |
| | | Run multi-file program |
| | | Compile multiple files in one command |
| | | Run single-command multi-file program |
| test_gcc_code_coverage_gcov | 4 cases | Compile with coverage flags |
| | | Run coverage test program |
| | | Run gcov |
| | | Check gcov output file exists |
| test_gcc_error_handling | 1 cases | Test type mismatch warning |
| test_gcc_special_features | 5 cases | Compile with C99 standard |
| | | Compile with __attribute__ |
| | | Run attribute test |
| | | Compile with -I include path |
| | | Run include path test |
| test_gcc_gcc_toolchain_utilities | 10 cases | gcc-ar version check |
| | | gcc-nm version check |
| | | gcc-ranlib version check |
| | | gcov-dump version check |
| | | gcov-tool version check |
| | | lto-dump version check |
| | | cc version check |
| | | cc equals gcc |
| | | c++ version check |
| | | c++ equals g++ |
