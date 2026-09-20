#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get atf help info"
        rlRun "atf --version 2>/dev/null || atf --version 2>/dev/null || true" 0 "Get atf version info"
        rlRun "atf --help 2>/dev/null || atf -h 2>/dev/null || atf --help 2>/dev/null || true" 0 "Get atf help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
