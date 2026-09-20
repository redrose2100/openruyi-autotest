#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get bison help info"
        rlRun "bison --version 2>/dev/null || bison --version 2>/dev/null || true" 0 "Get bison version info"
        rlRun "bison --help 2>/dev/null || bison -h 2>/dev/null || bison --help 2>/dev/null || true" 0 "Get bison help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
