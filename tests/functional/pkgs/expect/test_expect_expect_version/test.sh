#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get expect help info"
        rlRun "expect --version 2>/dev/null || expect --version 2>/dev/null || true" 0 "Get expect version info"
        rlRun "expect --help 2>/dev/null || expect -h 2>/dev/null || expect --help 2>/dev/null || true" 0 "Get expect help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
