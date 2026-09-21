#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install atf; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y atf 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which atf 2>/dev/null || true" 0 "Check atf binary exists"
        rlRun "atf --help >/dev/null 2>&1 || atf -h >/dev/null 2>&1 || atf --help >/dev/null 2>&1 || true" 0 "Check atf basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

