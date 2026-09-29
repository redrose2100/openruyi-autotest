#!/bin/bash

# Functional test: cmake - Error-handling

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



    rlPhaseStartTest "Error-handling"

    rlRun "cmake /nonexistent/path 2>&1" 1 "cmake vsdoes not existpathshould error"

    rlRun "cmake --build /nonexistent/build 2>&1" 1 "cmake --build vsdoes not existdirectoryshould error"

    rlRun "cmake -E true" 0 "cmake -E true returnsuccess"

    rlRun "cmake -E false 2>&1" 1 "cmake -E false returnfailed"

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