#!/bin/bash
# Functional test: openssh-clients - clients - ssh-agent
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

    rlPhaseStartTest "clients - ssh-agent"
    rlRun "ssh-add -l 2>&1 " 0 "ssh-add: list keys"
    rlRun "ssh-add test_key 2>&1" 0 "ssh-add: add key"
    rlRun "ssh-add -l 2>&1" 0 "ssh-add: verify key added"
    rlRun "ssh-add -L 2>&1" 0 "ssh-add -L: list public keys"
    rlRun "ssh-add -d test_key 2>&1" 0 "ssh-add -d: remove key"
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
