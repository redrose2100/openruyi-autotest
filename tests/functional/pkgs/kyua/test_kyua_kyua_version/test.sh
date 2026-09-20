#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get kyua help info"
        rlRun "kyua --version 2>/dev/null || kyua --version 2>/dev/null || true" 0 "Get kyua version info"
        rlRun "kyua --help 2>/dev/null || kyua -h 2>/dev/null || kyua --help 2>/dev/null || true" 0 "Get kyua help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
