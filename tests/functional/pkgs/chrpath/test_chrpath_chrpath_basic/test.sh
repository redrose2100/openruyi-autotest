#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which chrpath 2>/dev/null || which chrpath 2>/dev/null" 0 "Check chrpath is installed"
        rlRun "chrpath --help >/dev/null 2>&1 || chrpath -h >/dev/null 2>&1 || chrpath --help >/dev/null 2>&1" 0 "Check chrpath basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
