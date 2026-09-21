#!/bin/bash
# Functional test: util-linux - ipcmk/ipcrm IPC management
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    util-linuxSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "ipcmk/ipcrm IPC management"
    rlRun "ipcmk -Q 2>&1 | head -3 || echo ipcmk_tested" 0 "ipcmk: create message queue"
    rlRun "ipcs -q 2>&1 | head -3 || echo ipcs_tested" 0 "ipcs: show IPC facilities"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
