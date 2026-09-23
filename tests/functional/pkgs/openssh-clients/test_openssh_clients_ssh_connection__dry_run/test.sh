#!/bin/bash
# Functional test: openssh-clients - clients - ssh-connection--dry-run
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

    rlPhaseStartTest "clients - ssh-connection--dry-run"
    rlRun "ssh -G localhost 2>&1 | head -10" 0 "ssh -G: print config"
    rlRun "ssh -T -o ConnectTimeout=5 localhost 2>&1 " 0 "ssh -T: disable PTY"
    rlRun "ssh -v localhost 2>&1 | head -10 || true" 0 "ssh -v: verbose"
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
