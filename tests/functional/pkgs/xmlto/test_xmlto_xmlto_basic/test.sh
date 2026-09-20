#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which xmlto 2>/dev/null || which xmlto 2>/dev/null" 0 "Check xmlto is installed"
        rlRun "xmlto --help >/dev/null 2>&1 || xmlto -h >/dev/null 2>&1 || xmlto --help >/dev/null 2>&1" 0 "Check xmlto basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
