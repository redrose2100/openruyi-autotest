#!/bin/bash
# Functional test: systemd - hostnamectl---Hostname-management
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

    rlPhaseStartTest "hostnamectl---Hostname-management"
    rlRun "hostnamectl --version 2>&1 " 0 "hostnamectl version"
    rlRun "hostnamectl status" 0 "hostnamectl status: system info"
    rlRun "hostnamectl hostname" 0 "hostnamectl hostname: current name"
    rlRun "hostnamectl --static" 0 "hostnamectl --static"
    rlRun "hostnamectl --transient" 0 "hostnamectl --transient"
    rlRun "hostnamectl --pretty 2>&1 " 0 "hostnamectl --pretty"
    rlRun "hostnamectl chassis 2>&1 " 0 "hostnamectl chassis"
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
