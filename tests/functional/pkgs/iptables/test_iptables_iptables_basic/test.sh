#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Check main tool executability"
        rlRun "which iptables 2>/dev/null || which iptables 2>/dev/null" 0 "Check iptables is installed"
        rlRun "iptables --help >/dev/null 2>&1 || iptables -h >/dev/null 2>&1 || iptables --help >/dev/null 2>&1" 0 "Check iptables basic executability"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
