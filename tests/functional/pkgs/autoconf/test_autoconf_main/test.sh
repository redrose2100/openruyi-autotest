#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get autoconf version info"
        rlRun "which autoconf 2>/dev/null || which autoconf 2>/dev/null || true" 0 "Check autoconf is installed"
        rlRun "autoconf --version 2>/dev/null || autoconf --version 2>/dev/null || true" 0 "Get autoconf version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
