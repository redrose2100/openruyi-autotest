#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y gdb 2>/dev/null || rpm -q gdb" 0 "Ensure gdb is installed"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which gdb 2>/dev/null" 0 "Check gdb binary exists"
        rlRun "gdb --help >/dev/null 2>&1 || gdb -h >/dev/null 2>&1 || gdb --help >/dev/null 2>&1" 0 "Check gdb basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
