#!/bin/bash
# Functional test: openssh - RSA-key-generation
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensshSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "RSA-key-generation"
    rlRun "ssh-keygen -t rsa -b 2048 -f test_rsa -N \"\" -q" 0 "Generate RSA 2048 key"
    rlRun "test -f test_rsa" 0 "Private key exists"
    rlRun "test -f test_rsa.pub" 0 "Public key exists"
    rlRun "ssh-keygen -l -f test_rsa" 0 "Show RSA key fingerprint"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # openssh Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
