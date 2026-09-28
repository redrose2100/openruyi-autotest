#!/bin/bash
# Functional test: openssh-clients - clients - ssh-version-and-help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensshClientsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "clients - ssh-version-and-help"
    rlRun "ssh -V 2>&1" 0 "ssh version"
    rlRun "ssh -Q key 2>&1 | head -10" 0 "ssh -Q key: supported keys"
    rlRun "ssh -Q cipher 2>&1 | head -5" 0 "ssh -Q cipher: ciphers"
    rlRun "ssh -Q mac 2>&1 | head -5" 0 "ssh -Q mac: MACs"
    rlRun "ssh -Q kex 2>&1 | head -5" 0 "ssh -Q kex: key exchange"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # openssh-clients Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
