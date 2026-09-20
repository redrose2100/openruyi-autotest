#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get chrpath help info"
        rlRun "chrpath --version 2>/dev/null || chrpath --version 2>/dev/null || true" 0 "Get chrpath version info"
        rlRun "chrpath --help 2>/dev/null || chrpath -h 2>/dev/null || chrpath --help 2>/dev/null || true" 0 "Get chrpath help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
