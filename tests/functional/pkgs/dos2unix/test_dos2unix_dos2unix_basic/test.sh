#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which dos2unix 2>/dev/null || which dos2unix 2>/dev/null" 0 "Check dos2unix is installed"
        rlRun "dos2unix --help >/dev/null 2>&1 || dos2unix -h >/dev/null 2>&1 || dos2unix --help >/dev/null 2>&1" 0 "Check dos2unix basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
