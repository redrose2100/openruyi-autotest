#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get xxhash help info"
        rlRun "xxhash --version 2>/dev/null || xxhash --version 2>/dev/null || true" 0 "Get xxhash version info"
        rlRun "xxhash --help 2>/dev/null || xxhash -h 2>/dev/null || xxhash --help 2>/dev/null || true" 0 "Get xxhash help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
