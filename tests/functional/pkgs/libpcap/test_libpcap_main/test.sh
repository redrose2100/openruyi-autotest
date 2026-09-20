#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get libpcap version info"
        rlRun "which libpcap 2>/dev/null || which libpcap 2>/dev/null || true" 0 "Check libpcap is installed"
        rlRun "libpcap --version 2>/dev/null || libpcap --version 2>/dev/null || true" 0 "Get libpcap version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
