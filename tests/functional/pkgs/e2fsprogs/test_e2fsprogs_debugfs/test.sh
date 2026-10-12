#!/bin/bash
# Functional test: e2fsprogs - debugfs filesystem debugging tool
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
        dd if=/dev/zero of="$TestImg" bs=1M count=50 2>/dev/null
        rlRun "mkfs.ext4 -F -E nodiscard $TestImg 2>/dev/null" 0 "Create ext4 filesystem image"
        rlRun "mount -o loop $TestImg $MountPt" 0 "Mount loop device"
        echo "test content for debugfs" > "$MountPt/testfile.txt"
        mkdir "$MountPt/testdir"
        sync
    rlPhaseEnd

    rlPhaseStartTest "debugfs list files in image"
        rlRun "debugfs -R 'ls -l' $TestImg 2>/dev/null | grep -q testfile" 0 "debugfs lists testfile.txt"
    rlPhaseEnd

    rlPhaseStartTest "debugfs stat command"
        rlRun "debugfs -R 'stat testfile.txt' $TestImg 2>/dev/null | grep -qiE 'inode|File|size'" 0 "debugfs stat shows inode info"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "umount $MountPt 2>/dev/null" 0 "Unmount loop device"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd