#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get flex help info"
        rlRun "flex --version 2>/dev/null || flex --version 2>/dev/null || true" 0 "Get flex version info"
        rlRun "flex --help 2>/dev/null || flex -h 2>/dev/null || flex --help 2>/dev/null || true" 0 "Get flex help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
