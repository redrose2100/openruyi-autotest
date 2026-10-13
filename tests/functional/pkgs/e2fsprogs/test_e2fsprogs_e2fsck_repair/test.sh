#!/bin/bash
# Functional test: e2fsprogs - e2fsck filesystem check and repair
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        e2fsprogsSetup
        SUDO_PW="${TEST_SERVER_1_PASSWORD:-openruyi}"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        TestImg="$TmpDir/test_disk.img"
        MountPt="$TmpDir/mount"
        mkdir -p "$MountPt"
        dd if=/dev/zero of="$TestImg" bs=1M count=20 2>/dev/null
        rlRun "mkfs.ext4 -F $TestImg 2>/dev/null" 0 "Create ext4 filesystem image"
        # mount -o loop needs CAP_SYS_ADMIN, so run it via sudo.
        rlRun "echo '$SUDO_PW' | sudo -S mount -o loop $TestImg $MountPt" 0 "Mount loop device"
        rlRun "echo '$SUDO_PW' | sudo -S chown -R $(whoami) $MountPt" 0 "Take ownership of mount point"
        echo "test data" > "$MountPt/testfile"
        rlRun "grep test $MountPt/testfile" 0 "Verify file content"
        rlRun "echo '$SUDO_PW' | sudo -S umount $MountPt" 0 "Unmount filesystem"
    rlPhaseEnd

    rlPhaseStartTest "e2fsck check clean filesystem"
        rlRun "e2fsck -n $TestImg 2>/dev/null" 0 "e2fsck -n checks clean filesystem"
    rlPhaseEnd

    rlPhaseStartTest "e2fsck automatic repair"
        # Corrupt and repair
        dd if=/dev/zero of="$TestImg" bs=512 count=3 conv=notrunc 2>/dev/null
        # e2fsck returns 1 when it fixes errors, which is the expected outcome here.
        rlRun "e2fsck -y $TestImg 2>/dev/null" 1 "e2fsck -y repairs corrupted filesystem"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd