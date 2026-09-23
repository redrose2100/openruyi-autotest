#!/bin/bash
# Functional test: systemd - loginctl---Login-management
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

    rlPhaseStartTest "loginctl---Login-management"
    rlRun "loginctl --version 2>&1 " 0 "loginctl version"
    rlRun "loginctl list-sessions" 0 "loginctl list-sessions"
    rlRun "loginctl list-users" 0 "loginctl list-users"
    rlRun "loginctl show-session 2>&1 | head -10" 0 "loginctl show-session"
    rlRun "loginctl show-user openruyi 2>&1 | head -10" 0 "loginctl show-user"
    rlRun "loginctl user-status openruyi 2>&1 | head -10" 0 "loginctl user-status"
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
