#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y help2man 2>/dev/null || rpm -q help2man" 0 "Ensure help2man is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which help2man 2>/dev/null" 0 "Check help2man binary exists"
        rlRun "help2man --help >/dev/null 2>&1 || help2man -h >/dev/null 2>&1 || help2man --help >/dev/null 2>&1" 0 "Check help2man basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
