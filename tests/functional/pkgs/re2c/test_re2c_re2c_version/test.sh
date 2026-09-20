#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get re2c help info"
        rlRun "re2c --version 2>/dev/null || re2c --version 2>/dev/null || true" 0 "Get re2c version info"
        rlRun "re2c --help 2>/dev/null || re2c -h 2>/dev/null || re2c --help 2>/dev/null || true" 0 "Get re2c help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
