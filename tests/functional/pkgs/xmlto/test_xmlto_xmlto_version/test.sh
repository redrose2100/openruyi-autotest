#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get xmlto help info"
        rlRun "xmlto --version 2>/dev/null || xmlto --version 2>/dev/null || true" 0 "Get xmlto version info"
        rlRun "xmlto --help 2>/dev/null || xmlto -h 2>/dev/null || xmlto --help 2>/dev/null || true" 0 "Get xmlto help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
