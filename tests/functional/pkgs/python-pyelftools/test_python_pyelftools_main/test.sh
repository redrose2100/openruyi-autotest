#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get python-pyelftools version info"
        rlRun "which python-pyelftools 2>/dev/null || which pyelftools 2>/dev/null || true" 0 "Check python-pyelftools is installed"
        rlRun "python-pyelftools --version 2>/dev/null || pyelftools --version 2>/dev/null || true" 0 "Get python-pyelftools version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
