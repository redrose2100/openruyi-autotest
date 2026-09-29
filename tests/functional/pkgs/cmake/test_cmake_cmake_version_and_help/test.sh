#!/bin/bash

# Functional test: cmake - CMake-version-and-help

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



    rlPhaseStartTest "CMake-version-and-help"

    rlRun "cmake --version" 0 "check cmake version info"

    rlRun "cmake --help 2>&1 | grep -q Usage" 0 "cmake --help Show usage"

    rlRun "cmake --help-full 2>&1 | grep -q cmake" 0 "cmake --help-full displayfull"

    rlRun "cmake --help-command list 2>&1 | grep -q list" 0 "cmake --help-command list display list command"

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