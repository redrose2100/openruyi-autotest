#!/bin/bash

# Functional test: filesystem - error handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    filesystemSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "error handling"

    rlRun "ls /etc/" 0 "ls normaldirectorysuccess"

    rlRun "ls /nonexistent_12345 2>&1" 2 "ls does not existdirectoryshould error"

    rlRun "touch $TmpDir/testfile && test -f $TmpDir/testfile" 0 "touch and test -f basic functionality"

    rlRun "test -f /nonexistent_file 2>&1" 1 "test -f does not existfileshouldreturn 1"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # filesystem Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

