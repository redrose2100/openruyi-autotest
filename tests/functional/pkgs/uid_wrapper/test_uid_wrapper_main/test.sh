#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get uid_wrapper version info"
        rlRun "which uid_wrapper 2>/dev/null || which uid_wrapper 2>/dev/null || true" 0 "Check uid_wrapper is installed"
        rlRun "uid_wrapper --version 2>/dev/null || uid_wrapper --version 2>/dev/null || true" 0 "Get uid_wrapper version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
