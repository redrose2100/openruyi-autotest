#!/bin/bash

# Functional test: cmake - Basic-CMake-project

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    cmakeSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "Basic-CMake-project"

    rlRun "echo 'cmake_minimum_required(VERSION 3.10)' > $TmpDir/CMakeLists.txt" 0 "create CMakeLists.txt"

    rlRun "echo 'project(TestProject)' >> $TmpDir/CMakeLists.txt" 0 "add project declared"

    rlRun "echo 'add_executable(hello hello.c)' >> $TmpDir/CMakeLists.txt" 0 "addcanExecutetarget"

    rlRun "echo 'int main(){return 0;}' > $TmpDir/hello.c" 0 "createsource file"

    rlRun "cmake -S $TmpDir -B $TmpDir/build" 0 "cmake configurationitems"

    rlRun "test -f $TmpDir/build/CMakeCache.txt" 0 "verify CMakeCache.txt alreadyGenerate"

    rlRun "cmake --build $TmpDir/build" 0 "cmake builditems"

    rlRun "test -x $TmpDir/build/hello" 0 "verifyexecutablealreadyGenerate"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # cmake Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd


# pkgs-group-1-test v1