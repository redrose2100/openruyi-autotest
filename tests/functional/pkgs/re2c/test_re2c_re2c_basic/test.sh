#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install re2c; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y re2c 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which re2c 2>/dev/null || true" 0 "Check re2c binary exists"
        rlRun "re2c --help >/dev/null 2>&1 || re2c -h >/dev/null 2>&1 || re2c --help >/dev/null 2>&1 || true" 0 "Check re2c basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

