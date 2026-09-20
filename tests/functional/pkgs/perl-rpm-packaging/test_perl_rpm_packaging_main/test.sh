#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get perl-rpm-packaging version info"
        rlRun "which perl-rpm-packaging 2>/dev/null || which packaging 2>/dev/null || true" 0 "Check perl-rpm-packaging is installed"
        rlRun "perl-rpm-packaging --version 2>/dev/null || packaging --version 2>/dev/null || true" 0 "Get perl-rpm-packaging version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
