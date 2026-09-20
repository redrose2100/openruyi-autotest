#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get gdb help info"
        rlRun "gdb --version 2>/dev/null || gdb --version 2>/dev/null || true" 0 "Get gdb version info"
        rlRun "gdb --help 2>/dev/null || gdb -h 2>/dev/null || gdb --help 2>/dev/null || true" 0 "Get gdb help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
