#!/bin/bash
# Functional test: systemd - systemd-cgls---Cgroup-listing
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

    rlPhaseStartTest "systemd-cgls---Cgroup-listing"
    rlRun "systemd-cgls 2>&1 | head -20" 0 "systemd-cgls: cgroup tree"
    rlRun "systemd-cgls -k 2>&1 | head -5" 0 "systemd-cgls -k: kernel threads"
    rlRun "systemd-cgls --no-pager 2>&1 | head -10" 0 "systemd-cgls --no-pager"
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

# pkgs-full-test-run v1
