#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y systemtap 2>/dev/null || rpm -q systemtap" 0 "Ensure systemtap is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which systemtap 2>/dev/null" 0 "Check systemtap binary exists"
        rlRun "systemtap --help >/dev/null 2>&1 || systemtap -h >/dev/null 2>&1 || systemtap --help >/dev/null 2>&1" 0 "Check systemtap basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
