#!/bin/bash
# Functional test: systemd - systemctl-service-operations
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

    rlPhaseStartTest "systemctl-service-operations"
    rlRun "systemctl try-restart systemd-journald.service 2>&1 " 0 "systemctl try-restart"
    rlRun "systemctl reload-or-restart systemd-journald.service 2>&1 " 0 "systemctl reload-or-restart"
    rlRun "systemctl reset-failed 2>&1 " 0 "systemctl reset-failed"
    rlRun "systemctl daemon-reload 2>&1 " 0 "systemctl daemon-reload"
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
