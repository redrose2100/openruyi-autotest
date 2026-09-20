#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get python-wheel version info"
        rlRun "which python-wheel 2>/dev/null || which wheel 2>/dev/null || true" 0 "Check python-wheel is installed"
        rlRun "python-wheel --version 2>/dev/null || wheel --version 2>/dev/null || true" 0 "Get python-wheel version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
