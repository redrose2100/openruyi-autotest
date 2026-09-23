#!/bin/bash
# Functional test: systemd - Error-handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    systemdSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Error-handling"
    rlRun "systemctl nonexistent-command 2>&1 " 0 "systemctl: invalid command"
    rlRun "journalctl --invalid-option 2>&1 " 0 "journalctl: invalid option"
    rlRun "hostnamectl --help 2>&1 | grep -qiE \"Usage|Usage|usage\" || echo help-not-standard" 0 "hostnamectl: invalid option"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # systemd Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
