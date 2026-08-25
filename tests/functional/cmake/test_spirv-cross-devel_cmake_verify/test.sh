#!/bin/bash
# Functional test: spirv-cross-devel - cmake export integrity verification
# Verify that all files referenced by .cmake files provided by the package actually exist
#
# Verification principle:
#   find_package(CONFIG) -> *Config.cmake -> *Targets.cmake
#   Targets.cmake referencing non-existent .a/.so will cause cmake configuration to fail directly

. /usr/share/beakerlib/beakerlib.sh || exit 1

PKG="spirv-cross-devel"

rlJournalStart
    rlPhaseStartSetup "Environment Setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"

        CMAKE_COUNT=$(rpm -ql "$PKG" 2>/dev/null | grep -c '\.cmake$' || echo 0)
        rlLogInfo "$PKG provides $CMAKE_COUNT .cmake file(s)"
    rlPhaseEnd

    rlPhaseStartTest "find_package(CONFIG) - Verify cmake export integrity"
        if [ "$CMAKE_COUNT" -eq 0 ]; then
            rlLogWarning "$PKG provides no .cmake files, skipping cmake verification"
        else
            # --- find_package(spirv_cross_c) ---
            # spirv_cross_c depends on: glsl, hlsl, msl, cpp, reflect
            # glsl/hlsl/msl/cpp depend on: core
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)
find_package(spirv_cross_glsl REQUIRED CONFIG)
find_package(spirv_cross_hlsl REQUIRED CONFIG)
find_package(spirv_cross_msl REQUIRED CONFIG)
find_package(spirv_cross_cpp REQUIRED CONFIG)
find_package(spirv_cross_reflect REQUIRED CONFIG)
find_package(spirv_cross_c REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_c) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_c CONFIG) ..."
            rm -rf "$TmpDir/build_0"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_0" 0 \
                "cmake configuration (find_package spirv_cross_c CONFIG)"; then
                rlPass "find_package(spirv_cross_c CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_c CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_c_shared) ---
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_c_shared REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_c_shared) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_c_shared CONFIG) ..."
            rm -rf "$TmpDir/build_1"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_1" 0 \
                "cmake configuration (find_package spirv_cross_c_shared CONFIG)"; then
                rlPass "find_package(spirv_cross_c_shared CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_c_shared CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_core) ---
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_core) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_core CONFIG) ..."
            rm -rf "$TmpDir/build_2"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_2" 0 \
                "cmake configuration (find_package spirv_cross_core CONFIG)"; then
                rlPass "find_package(spirv_cross_core CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_core CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_cpp) ---
            # spirv_cross_cpp depends on: glsl -> core
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)
find_package(spirv_cross_glsl REQUIRED CONFIG)
find_package(spirv_cross_cpp REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_cpp) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_cpp CONFIG) ..."
            rm -rf "$TmpDir/build_3"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_3" 0 \
                "cmake configuration (find_package spirv_cross_cpp CONFIG)"; then
                rlPass "find_package(spirv_cross_cpp CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_cpp CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_glsl) ---
            # spirv_cross_glsl depends on: core
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)
find_package(spirv_cross_glsl REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_glsl) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_glsl CONFIG) ..."
            rm -rf "$TmpDir/build_4"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_4" 0 \
                "cmake configuration (find_package spirv_cross_glsl CONFIG)"; then
                rlPass "find_package(spirv_cross_glsl CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_glsl CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_hlsl) ---
            # spirv_cross_hlsl depends on: glsl -> core
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)
find_package(spirv_cross_glsl REQUIRED CONFIG)
find_package(spirv_cross_hlsl REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_hlsl) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_hlsl CONFIG) ..."
            rm -rf "$TmpDir/build_5"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_5" 0 \
                "cmake configuration (find_package spirv_cross_hlsl CONFIG)"; then
                rlPass "find_package(spirv_cross_hlsl CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_hlsl CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_msl) ---
            # spirv_cross_msl depends on: glsl -> core
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)
find_package(spirv_cross_glsl REQUIRED CONFIG)
find_package(spirv_cross_msl REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_msl) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_msl CONFIG) ..."
            rm -rf "$TmpDir/build_6"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_6" 0 \
                "cmake configuration (find_package spirv_cross_msl CONFIG)"; then
                rlPass "find_package(spirv_cross_msl CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_msl CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_reflect) ---
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_reflect REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_reflect) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_reflect CONFIG) ..."
            rm -rf "$TmpDir/build_7"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_7" 0 \
                "cmake configuration (find_package spirv_cross_reflect CONFIG)"; then
                rlPass "find_package(spirv_cross_reflect CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_reflect CONFIG) verification failed"
            fi

            # --- find_package(spirv_cross_util) ---
            # spirv_cross_util depends on: core
            cat > "$TmpDir/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.13.4)
project(cmake_verify
  VERSION "0.1"
  LANGUAGES C CXX)

find_package(spirv_cross_core REQUIRED CONFIG)
find_package(spirv_cross_util REQUIRED CONFIG)

message(STATUS "find_package(spirv_cross_util) succeeded")
EOF

            rlLogInfo "Verifying find_package(spirv_cross_util CONFIG) ..."
            rm -rf "$TmpDir/build_8"
            if rlRun "cmake -S $TmpDir -B $TmpDir/build_8" 0 \
                "cmake configuration (find_package spirv_cross_util CONFIG)"; then
                rlPass "find_package(spirv_cross_util CONFIG) verification passed"
            else
                rlFail "find_package(spirv_cross_util CONFIG) verification failed"
            fi

        fi
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
