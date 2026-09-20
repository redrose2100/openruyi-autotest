#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which scdoc 2>/dev/null || which scdoc 2>/dev/null" 0 "Check scdoc is installed"
        rlRun "scdoc --help >/dev/null 2>&1 || scdoc -h >/dev/null 2>&1 || scdoc --help >/dev/null 2>&1" 0 "Check scdoc basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
