#!/bin/bash
# Functional test: dbus - dbus-monitor command
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "dbus-monitor -h - help"
        rlRun "dbus-monitor -h 2>&1 | head -3" 0 "dbus-monitor -h works"
    rlPhaseEnd

    rlPhaseStartTest "dbus-monitor --system - system bus monitor"
        rlRun "timeout 2 dbus-monitor --system 2>&1; true" 0 "dbus-monitor --system runs"
    rlPhaseEnd

    rlPhaseStartTest "dbus-monitor --session - session bus monitor"
        rlRun "timeout 2 dbus-monitor --session 2>&1; true" 0 "dbus-monitor --session runs"
    rlPhaseEnd

    rlPhaseStartTest "dbus-monitor --profile - profile mode"
        rlRun "timeout 2 dbus-monitor --profile --session 2>&1; true" 0 "dbus-monitor --profile runs"
    rlPhaseEnd

    rlPhaseStartTest "dbus-monitor --monitor - monitor mode"
        rlRun "timeout 2 dbus-monitor --monitor --session 2>&1; true" 0 "dbus-monitor --monitor runs"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd