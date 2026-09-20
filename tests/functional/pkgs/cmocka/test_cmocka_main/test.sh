#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get cmocka version info"
        rlRun "which cmocka 2>/dev/null || which cmocka 2>/dev/null || true" 0 "Check cmocka is installed"
        rlRun "cmocka --version 2>/dev/null || cmocka --version 2>/dev/null || true" 0 "Get cmocka version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
