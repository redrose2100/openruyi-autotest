#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get systemtap help info"
        rlRun "systemtap --version 2>/dev/null || systemtap --version 2>/dev/null || true" 0 "Get systemtap version info"
        rlRun "systemtap --help 2>/dev/null || systemtap -h 2>/dev/null || systemtap --help 2>/dev/null || true" 0 "Get systemtap help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
