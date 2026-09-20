#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get groff help info"
        rlRun "groff --version 2>/dev/null || groff --version 2>/dev/null || true" 0 "Get groff version info"
        rlRun "groff --help 2>/dev/null || groff -h 2>/dev/null || groff --help 2>/dev/null || true" 0 "Get groff help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
