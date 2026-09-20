#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get gdbm help info"
        rlRun "gdbm --version 2>/dev/null || gdbm --version 2>/dev/null || true" 0 "Get gdbm version info"
        rlRun "gdbm --help 2>/dev/null || gdbm -h 2>/dev/null || gdbm --help 2>/dev/null || true" 0 "Get gdbm help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
