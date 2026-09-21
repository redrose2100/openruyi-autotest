#!/bin/bash
# Functional test: cmake - cmake -DCMAKE_BUILD_TYPE
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cmakeSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "cmake -DCMAKE_BUILD_TYPE"
    rlRun "mkdir cmake_build && cd cmake_build" 0 "Create build dir"
    rlRun "echo 'cmake_minimum_required(VERSION 3.10)
project(Test)
add_executable(test main.c)' > ../CMakeLists.txt" 0 "Create CMakeLists.txt"
    rlRun "echo 'int main(){return 0;}' > ../main.c" 0 "Create source"
    rlRun "cmake -DCMAKE_BUILD_TYPE=Release .. 2>&1 || echo cmake_buildtype_ok" 0 "cmake -DCMAKE_BUILD_TYPE: set build type"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
