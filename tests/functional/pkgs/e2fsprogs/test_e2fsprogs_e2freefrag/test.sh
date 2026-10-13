#!/bin/bash
# Functional test: e2fsprogs - e2freefrag free space fragmentation analyzer
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        e2fsprogsSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        TestImg="$TmpDir/test_disk.img"
        dd if=/dev/zero of="$TestImg" bs=1M count=200 2>/dev/null
        rlRun "mkfs.ext4 -F $TestImg 2>/dev/null" 0 "Create ext4 filesystem image"
    rlPhaseEnd

    rlPhaseStartTest "e2freefrag basic report"
        rlRun "e2freefrag $TestImg 2>/dev/null" 0 "e2freefrag runs on ext4 image"
    rlPhaseEnd

    rlPhaseStartTest "e2freefrag with chunk size"
        rlRun "e2freefrag -c 4 $TestImg 2>/dev/null" 0 "e2freefrag reports with 4KB chunk size"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd