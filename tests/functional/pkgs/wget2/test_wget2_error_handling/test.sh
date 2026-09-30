#!/bin/bash

# Functional test: wget2 - Error-handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    wget2Setup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "Error-handling"

    rlRun "wget2 http://127.0.0.1:1/ 2>&1" 2 "wget2 connectionportshould error"

    rlRun "wget2 http://nonexistent.invalid/ 2>&1" 4 "wget2 Unable toresolve domain should error"

    rlRun "wget2 --invalid-option 2>&1" 1 "wget2 Invalid option should error"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # wget2 Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

