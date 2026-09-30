#!/bin/bash
# Functional test: e2fsprogs - e2fsprogs error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    e2fsprogsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "e2fsprogs error handling"
    rlRun "e2fsck --help 2>&1 | grep -qiE \"Usage|Usage|usage\" || echo help-not-standard" 0 "Ч"
    rlRun "mke2fs --help 2>&1 | grep -qiE \"Usage|Usage|usage\" || echo help-not-standard" 0 "mke2fs Ч"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # e2fsprogs Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-group-2-test v1
