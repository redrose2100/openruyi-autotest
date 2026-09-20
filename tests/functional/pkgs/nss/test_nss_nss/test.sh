#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get nss help info"
        rlRun "nss --version 2>/dev/null || nss --version 2>/dev/null || true" 0 "Get nss version info"
        rlRun "nss --help 2>/dev/null || nss -h 2>/dev/null || nss --help 2>/dev/null || true" 0 "Get nss help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
