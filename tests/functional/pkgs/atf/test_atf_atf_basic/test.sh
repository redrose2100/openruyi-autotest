#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which atf 2>/dev/null || which atf 2>/dev/null" 0 "Check atf is installed"
        rlRun "atf --help >/dev/null 2>&1 || atf -h >/dev/null 2>&1 || atf --help >/dev/null 2>&1" 0 "Check atf basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
