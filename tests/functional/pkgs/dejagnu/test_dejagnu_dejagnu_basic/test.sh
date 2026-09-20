#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which dejagnu 2>/dev/null || which dejagnu 2>/dev/null" 0 "Check dejagnu is installed"
        rlRun "dejagnu --help >/dev/null 2>&1 || dejagnu -h >/dev/null 2>&1 || dejagnu --help >/dev/null 2>&1" 0 "Check dejagnu basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
