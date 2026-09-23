#!/bin/bash
# Functional test: openssh - Ed25519-key-generation
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

    rlPhaseStartTest "Ed25519-key-generation"
    rlRun "ssh-keygen -t ed25519 -f test_ed25519 -N \"\" -q" 0 "Generate Ed25519 key"
    rlRun "ssh-keygen -l -f test_ed25519.pub" 0 "Show Ed25519 fingerprint"
    rlRun "ssh-keygen -l -v -f test_ed25519.pub 2>&1 " 0 "Verbose fingerprint"
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
