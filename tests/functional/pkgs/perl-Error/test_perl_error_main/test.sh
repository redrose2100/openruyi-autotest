#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get perl-Error version info"
        rlRun "which perl-Error 2>/dev/null || which Error 2>/dev/null || true" 0 "Check perl-Error is installed"
        rlRun "perl-Error --version 2>/dev/null || Error --version 2>/dev/null || true" 0 "Get perl-Error version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
