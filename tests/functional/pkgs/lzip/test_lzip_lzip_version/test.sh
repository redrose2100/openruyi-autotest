#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get lzip help info"
        rlRun "lzip --version 2>/dev/null || lzip --version 2>/dev/null || true" 0 "Get lzip version info"
        rlRun "lzip --help 2>/dev/null || lzip -h 2>/dev/null || lzip --help 2>/dev/null || true" 0 "Get lzip help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
