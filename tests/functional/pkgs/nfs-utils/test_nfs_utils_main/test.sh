#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get nfs-utils version info"
        rlRun "which nfs-utils 2>/dev/null || which utils 2>/dev/null || true" 0 "Check nfs-utils is installed"
        rlRun "nfs-utils --version 2>/dev/null || utils --version 2>/dev/null || true" 0 "Get nfs-utils version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
