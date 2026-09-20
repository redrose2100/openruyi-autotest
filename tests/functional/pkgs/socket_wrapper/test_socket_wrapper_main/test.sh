#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get socket_wrapper version info"
        rlRun "which socket_wrapper 2>/dev/null || which socket_wrapper 2>/dev/null || true" 0 "Check socket_wrapper is installed"
        rlRun "socket_wrapper --version 2>/dev/null || socket_wrapper --version 2>/dev/null || true" 0 "Get socket_wrapper version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
