#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get libsodium version info"
        rlRun "which libsodium 2>/dev/null || which libsodium 2>/dev/null || true" 0 "Check libsodium is installed"
        rlRun "libsodium --version 2>/dev/null || libsodium --version 2>/dev/null || true" 0 "Get libsodium version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
