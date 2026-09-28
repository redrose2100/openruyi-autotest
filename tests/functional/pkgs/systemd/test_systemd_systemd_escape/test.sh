#!/bin/bash
# Functional test: systemd - systemd-escape
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

    rlPhaseStartTest "systemd-escape"
    rlRun "systemd-escape \"hello world\"" 0 "systemd-escape: basic escape"
    rlRun "systemd-escape --path \"/usr/bin/test\"" 0 "systemd-escape --path: path escape"
    rlRun "systemd-escape -u \"hello\\x20world\"" 0 "systemd-escape -u: unescape"
    rlRun "systemd-escape --suffix=mount \"/mnt/data\"" 0 "systemd-escape --suffix"
    rlRun "systemd-escape --template=\"test@.service\" instance" 0 "systemd-escape --template"
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
