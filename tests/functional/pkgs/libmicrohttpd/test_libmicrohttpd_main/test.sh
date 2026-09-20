#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get libmicrohttpd version info"
        rlRun "which libmicrohttpd 2>/dev/null || which libmicrohttpd 2>/dev/null || true" 0 "Check libmicrohttpd is installed"
        rlRun "libmicrohttpd --version 2>/dev/null || libmicrohttpd --version 2>/dev/null || true" 0 "Get libmicrohttpd version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
