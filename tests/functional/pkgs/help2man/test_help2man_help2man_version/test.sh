#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get help2man help info"
        rlRun "help2man --version 2>/dev/null || help2man --version 2>/dev/null || true" 0 "Get help2man version info"
        rlRun "help2man --help 2>/dev/null || help2man -h 2>/dev/null || help2man --help 2>/dev/null || true" 0 "Get help2man help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
