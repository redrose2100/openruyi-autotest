#!/bin/bash
# Functional test: systemd - systemd-detect-virt
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

    rlPhaseStartTest "systemd-detect-virt"
    rlRun "systemd-detect-virt" 0 "systemd-detect-virt: detect VM"
    rlRun "systemd-detect-virt -q" 0 "systemd-detect-virt -q: quiet mode"
    rlRun "systemd-detect-virt -c 2>&1 " 0 "systemd-detect-virt -c: container only"
    rlRun "systemd-detect-virt -v 2>&1 " 0 "systemd-detect-virt -v: VM only"
    rlRun "systemd-detect-virt -r 2>&1 " 0 "systemd-detect-virt -r: chroot only"
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
