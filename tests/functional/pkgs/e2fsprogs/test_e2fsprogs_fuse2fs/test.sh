#!/bin/bash
# Functional test: e2fsprogs - fuse2fs userspace filesystem
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        e2fsprogsSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        TestImg="$TmpDir/test.img"
        MntDir="$TmpDir/fuse_mnt"
        mkdir -p "$MntDir"
        dd if=/dev/zero of="$TestImg" bs=1M count=100 2>/dev/null
        rlRun "mkfs.ext4 -F $TestImg 2>/dev/null" 0 "Create ext4 filesystem image"
    rlPhaseEnd

    rlPhaseStartTest "fuse2fs read-write mount"
        rlRun "fuse2fs $TestImg $MntDir 2>/dev/null" 0 "fuse2fs mounts image read-write"
        rlRun "echo 'test_content' > $MntDir/test.txt" 0 "Write file in fuse2fs mount"
        rlRun "grep -q 'test_content' $MntDir/test.txt" 0 "Read file from fuse2fs mount"
        rlRun "fusermount -u $MntDir 2>/dev/null" 0 "Unmount fuse2fs filesystem"
    rlPhaseEnd

    rlPhaseStartTest "fuse2fs read-only mount"
        rlRun "fuse2fs -o ro $TestImg $MntDir 2>/dev/null" 0 "fuse2fs mounts read-only"
        touch "$MntDir/test2.txt" 2>/dev/null
        rlRun "test $? -ne 0" 0 "Write fails on read-only mount"
        rlRun "fusermount -u $MntDir 2>/dev/null" 0 "Unmount read-only filesystem"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "fusermount -u $MntDir 2>/dev/null || true" 0 "Ensure unmount"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd