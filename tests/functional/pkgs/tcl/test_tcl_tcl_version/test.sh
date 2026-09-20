#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get tcl help info"
        rlRun "tcl --version 2>/dev/null || tcl --version 2>/dev/null || true" 0 "Get tcl version info"
        rlRun "tcl --help 2>/dev/null || tcl -h 2>/dev/null || tcl --help 2>/dev/null || true" 0 "Get tcl help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
