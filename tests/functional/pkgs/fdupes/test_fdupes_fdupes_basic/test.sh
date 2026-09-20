#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which fdupes 2>/dev/null || which fdupes 2>/dev/null" 0 "Check fdupes is installed"
        rlRun "fdupes --help >/dev/null 2>&1 || fdupes -h >/dev/null 2>&1 || fdupes --help >/dev/null 2>&1" 0 "Check fdupes basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
