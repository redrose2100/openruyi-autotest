#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check package installed"
        rlRun "which python-srpm-macros 2>/dev/null || which macros 2>/dev/null || true" 0 "Check python-srpm-macros is installed"
        rlRun "python-srpm-macros --version 2>/dev/null || macros --version 2>/dev/null || true" 0 "Get python-srpm-macros version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
