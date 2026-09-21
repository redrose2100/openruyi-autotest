#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y xxhash 2>/dev/null || rpm -q xxhash" 0 "Ensure xxhash is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which xxhash 2>/dev/null" 0 "Check xxhash binary exists"
        rlRun "xxhash --help >/dev/null 2>&1 || xxhash -h >/dev/null 2>&1 || xxhash --help >/dev/null 2>&1" 0 "Check xxhash basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
