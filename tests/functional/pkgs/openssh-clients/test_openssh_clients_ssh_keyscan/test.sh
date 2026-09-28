#!/bin/bash
# Functional test: openssh-clients - clients - ssh-keyscan
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

    rlPhaseStartTest "clients - ssh-keyscan"
    rlRun "ssh-keyscan -t ed25519 localhost 2>&1 | head -3" 0 "ssh-keyscan: scan localhost"
    rlRun "ssh-keyscan -t rsa localhost 2>&1 | head -3" 0 "ssh-keyscan -t rsa"
    rlRun "ssh-keyscan -t ecdsa localhost 2>&1 | head -3" 0 "ssh-keyscan -t ecdsa"
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
