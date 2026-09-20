#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get fdupes help info"
        rlRun "fdupes --version 2>/dev/null || fdupes --version 2>/dev/null || true" 0 "Get fdupes version info"
        rlRun "fdupes --help 2>/dev/null || fdupes -h 2>/dev/null || fdupes --help 2>/dev/null || true" 0 "Get fdupes help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
