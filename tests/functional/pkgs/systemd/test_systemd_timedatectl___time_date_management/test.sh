#!/bin/bash
# Functional test: systemd - timedatectl---Time-date-management
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

    rlPhaseStartTest "timedatectl---Time-date-management"
    rlRun "timedatectl --version 2>&1 " 0 "timedatectl version"
    rlRun "timedatectl status" 0 "timedatectl status: time info"
    rlRun "timedatectl show" 0 "timedatectl show: all properties"
    rlRun "timedatectl list-timezones 2>&1 | head -10" 0 "timedatectl list-timezones"
    rlRun "timedatectl show-timesync 2>&1 | head -5" 0 "timedatectl show-timesync"
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
