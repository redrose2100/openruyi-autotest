#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y expect 2>/dev/null || rpm -q expect" 0 "Ensure expect is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which expect 2>/dev/null" 0 "Check expect binary exists"
        rlRun "expect --help >/dev/null 2>&1 || expect -h >/dev/null 2>&1 || expect --help >/dev/null 2>&1" 0 "Check expect basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
