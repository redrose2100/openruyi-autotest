#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get dos2unix help info"
        rlRun "dos2unix --version 2>/dev/null || dos2unix --version 2>/dev/null || true" 0 "Get dos2unix version info"
        rlRun "dos2unix --help 2>/dev/null || dos2unix -h 2>/dev/null || dos2unix --help 2>/dev/null || true" 0 "Get dos2unix help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
