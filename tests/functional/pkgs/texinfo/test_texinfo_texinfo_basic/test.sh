#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which texinfo 2>/dev/null || which texinfo 2>/dev/null" 0 "Check texinfo is installed"
        rlRun "texinfo --help >/dev/null 2>&1 || texinfo -h >/dev/null 2>&1 || texinfo --help >/dev/null 2>&1" 0 "Check texinfo basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
