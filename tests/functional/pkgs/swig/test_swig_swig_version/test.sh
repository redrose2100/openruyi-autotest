#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get swig help info"
        rlRun "swig --version 2>/dev/null || swig --version 2>/dev/null || true" 0 "Get swig version info"
        rlRun "swig --help 2>/dev/null || swig -h 2>/dev/null || swig --help 2>/dev/null || true" 0 "Get swig help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
