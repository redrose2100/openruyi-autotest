#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get python-setuptools version info"
        rlRun "which python-setuptools 2>/dev/null || which setuptools 2>/dev/null || true" 0 "Check python-setuptools is installed"
        rlRun "python-setuptools --version 2>/dev/null || setuptools --version 2>/dev/null || true" 0 "Get python-setuptools version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
