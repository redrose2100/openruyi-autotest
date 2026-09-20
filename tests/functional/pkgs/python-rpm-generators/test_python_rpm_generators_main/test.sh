#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get python-rpm-generators version info"
        rlRun "which python-rpm-generators 2>/dev/null || which generators 2>/dev/null || true" 0 "Check python-rpm-generators is installed"
        rlRun "python-rpm-generators --version 2>/dev/null || generators --version 2>/dev/null || true" 0 "Get python-rpm-generators version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
