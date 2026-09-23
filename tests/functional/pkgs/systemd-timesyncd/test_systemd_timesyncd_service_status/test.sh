#!/bin/bash
# Functional test: systemd-timesyncd - timesyncd - Service-status
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    systemdTimesyncdSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "timesyncd - Service-status"
    rlRun "systemctl status systemd-timesyncd.service 2>&1 | head -10" 0 "Service status"
    rlRun "timedatectl show-timesync 2>&1 | head -10" 0 "Time sync status"
    rlRun "timedatectl timesync-status 2>&1 | head -10" 0 "Timesync detail"
    rlRun "systemctl is-enabled systemd-timesyncd.service 2>&1 " 0 "Is enabled"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # systemd-timesyncd Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
