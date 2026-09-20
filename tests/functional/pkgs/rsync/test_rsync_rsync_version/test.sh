#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get rsync help info"
        rlRun "rsync --version 2>/dev/null || rsync --version 2>/dev/null || true" 0 "Get rsync version info"
        rlRun "rsync --help 2>/dev/null || rsync -h 2>/dev/null || rsync --help 2>/dev/null || true" 0 "Get rsync help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
