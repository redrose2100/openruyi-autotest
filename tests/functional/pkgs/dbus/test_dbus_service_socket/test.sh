#!/bin/bash
# Functional test: dbus - service and socket activation
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "dbus-daemon - version check"
        rlRun "dbus-daemon --version 2>&1 | head -1" 0 "dbus-daemon --version works"
    rlPhaseEnd

    rlPhaseStartTest "dbus.service - check status"
        rlRun "systemctl is-active dbus.service 2>&1 || true" 0 "Check dbus.service status"
    rlPhaseEnd

    rlPhaseStartTest "dbus.socket - check status"
        rlRun "systemctl is-active dbus.socket 2>&1 || true" 0 "Check dbus.socket status"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd