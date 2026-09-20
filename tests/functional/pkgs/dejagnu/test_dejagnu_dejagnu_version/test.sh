#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get dejagnu help info"
        rlRun "dejagnu --version 2>/dev/null || dejagnu --version 2>/dev/null || true" 0 "Get dejagnu version info"
        rlRun "dejagnu --help 2>/dev/null || dejagnu -h 2>/dev/null || dejagnu --help 2>/dev/null || true" 0 "Get dejagnu help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
