#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y lzip 2>/dev/null || rpm -q lzip" 0 "Ensure lzip is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which lzip 2>/dev/null" 0 "Check lzip binary exists"
        rlRun "lzip --help >/dev/null 2>&1 || lzip -h >/dev/null 2>&1 || lzip --help >/dev/null 2>&1" 0 "Check lzip basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
