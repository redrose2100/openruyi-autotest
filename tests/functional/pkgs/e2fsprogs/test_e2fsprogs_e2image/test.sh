#!/bin/bash
# Functional test: e2fsprogs - e2image metadata image creation
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        e2fsprogsSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        TestImg="$TmpDir/test_disk.img"
        MountPt="$TmpDir/mount"
        mkdir -p "$MountPt"
        dd if=/dev/zero of="$TestImg" bs=1M count=100 2>/dev/null
        rlRun "mkfs.ext4 -F $TestImg 2>/dev/null" 0 "Create ext4 filesystem image"
        rlRun "mount -o loop $TestImg $MountPt" 0 "Mount loop device"
        echo "test file content" > "$MountPt/testfile.txt"
        mkdir "$MountPt/testdir"
        echo "subdir file" > "$MountPt/testdir/subfile.txt"
        for i in $(seq 1 5); do
            echo "data $i" > "$MountPt/file_$i.txt"
        done
        sync
        rlRun "umount $MountPt" 0 "Unmount filesystem"
    rlPhaseEnd

    rlPhaseStartTest "e2image create metadata image"
        rlRun "e2image $TestImg $TmpDir/metadata.img 2>/dev/null" 0 "e2image creates metadata image"
        rlRun "test -f $TmpDir/metadata.img" 0 "Metadata image file exists"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd