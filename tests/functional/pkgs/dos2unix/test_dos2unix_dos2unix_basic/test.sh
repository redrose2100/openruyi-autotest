#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y dos2unix 2>/dev/null || rpm -q dos2unix" 0 "Ensure dos2unix is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which dos2unix 2>/dev/null" 0 "Check dos2unix binary exists"
        rlRun "dos2unix --help >/dev/null 2>&1 || dos2unix -h >/dev/null 2>&1 || dos2unix --help >/dev/null 2>&1" 0 "Check dos2unix basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
