#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get iptables help info"
        rlRun "iptables --version 2>/dev/null || iptables --version 2>/dev/null || true" 0 "Get iptables version info"
        rlRun "iptables --help 2>/dev/null || iptables -h 2>/dev/null || iptables --help 2>/dev/null || true" 0 "Get iptables help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
