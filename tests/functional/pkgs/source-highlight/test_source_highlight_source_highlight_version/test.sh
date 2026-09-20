#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get source-highlight help info"
        rlRun "source-highlight --version 2>/dev/null || highlight --version 2>/dev/null || true" 0 "Get source-highlight version info"
        rlRun "source-highlight --help 2>/dev/null || source-highlight -h 2>/dev/null || highlight --help 2>/dev/null || true" 0 "Get source-highlight help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
