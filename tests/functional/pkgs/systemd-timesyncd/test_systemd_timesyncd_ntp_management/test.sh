#!/bin/bash
# Functional test: systemd-timesyncd - timesyncd - NTP-management
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

    rlPhaseStartTest "timesyncd - NTP-management"
    rlRun "timedatectl show-timesync --property=FallbackNTPServers 2>&1 " 0 "Fallback NTP servers"
    rlRun "timedatectl show-timesync --property=ServerName 2>&1 " 0 "Current NTP server"
    rlRun "timedatectl show-timesync --property=ServerAddress 2>&1 " 0 "Server address"
    rlRun "timedatectl ntp-servers 2>&1 " 0 "NTP servers list"
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
