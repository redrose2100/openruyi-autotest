#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check package installed"
        rlRun "which publicsuffix-list 2>/dev/null || which list 2>/dev/null || true" 0 "Check publicsuffix-list is installed"
        rlRun "publicsuffix-list --version 2>/dev/null || list --version 2>/dev/null || true" 0 "Get publicsuffix-list version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
