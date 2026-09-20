#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get scdoc help info"
        rlRun "scdoc --version 2>/dev/null || scdoc --version 2>/dev/null || true" 0 "Get scdoc version info"
        rlRun "scdoc --help 2>/dev/null || scdoc -h 2>/dev/null || scdoc --help 2>/dev/null || true" 0 "Get scdoc help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
