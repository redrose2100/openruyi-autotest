#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y dejagnu 2>/dev/null || rpm -q dejagnu" 0 "Ensure dejagnu is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which dejagnu 2>/dev/null" 0 "Check dejagnu binary exists"
        rlRun "dejagnu --help >/dev/null 2>&1 || dejagnu -h >/dev/null 2>&1 || dejagnu --help >/dev/null 2>&1" 0 "Check dejagnu basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
