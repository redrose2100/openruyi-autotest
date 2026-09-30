#!/bin/bash
# Functional test: cloud-utils-growpart - utils-growpart - Disk-partition-info
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cloudUtilsGrowpartSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "utils-growpart - Disk-partition-info"
    rlRun "lsblk 2>&1 | head -10" 0 "lsblk: list block devices"
    rlRun "df -h | head -10" 0 "df: disk free space"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # cloud-utils-growpart Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
