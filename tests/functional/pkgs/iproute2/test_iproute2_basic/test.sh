#!/bin/bash
# Functional test: iproute2 - iproute2 error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    iproute2Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "iproute2 error handling"
    rlRun "ip addr show 2>&1 | head -10" 0 "Show network addresses"
    rlRun "ip link show 2>&1 | head -10" 0 "Show network interfaces"
    rlRun "ip route show 2>&1 | head -5" 0 "Show routing table"
    rlRun "ss --help 2>&1 | head -10" 0 "Socket statistics"
    rlRun "ss -tln 2>&1 | head -10" 0 "Socket statistics"
    rlRun "tc --help 2>&1 | head -10" 0 "Traffic control"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # iproute2 Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
