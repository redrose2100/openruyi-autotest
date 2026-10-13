#!/bin/bash
# Functional test: cpio - advanced options (-v, -d, -m, -a, -L, -n)
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo 'file1' > f1
        echo 'file2' > f2
        mkdir dir1
        echo 'dir1/file3' > dir1/file3
    rlPhaseEnd

    rlPhaseStartTest "cpio -v - verbose mode"
        rlRun "printf 'f1\nf2\n' | cpio -ov > archive.cpio 2>&1" 0 "cpio -v creates archive with verbose output"
    rlPhaseEnd

    rlPhaseStartTest "cpio -d - create leading directories"
        rlRun "printf 'dir1/file3\n' | cpio -o > archive2.cpio 2>/dev/null" 0 "Create archive with subdirectory"
        mkdir extract_dir && cd extract_dir
        rlRun "cpio -id < ../archive2.cpio 2>/dev/null && test -f dir1/file3" 0 "cpio -d creates parent directories on extract"
        cd ..
    rlPhaseEnd

    rlPhaseStartTest "cpio -a - reset access times"
        rlRun "printf 'f1\nf2\n' | cpio -oa > archive_a.cpio 2>/dev/null" 0 "cpio -a resets access time"
    rlPhaseEnd

    rlPhaseStartTest "cpio -m - preserve modification times"
        printf 'f1\n' | cpio -o > archive_m.cpio 2>/dev/null
        original_mtime=$(stat -c %Y f1)
        mkdir extract_m
        ( cd extract_m && cpio -idm < ../archive_m.cpio >/dev/null 2>&1 )
        extracted_mtime=$(stat -c %Y extract_m/f1)
        rlAssertEquals "cpio -m preserves modification time on extract" "$original_mtime" "$extracted_mtime"
    rlPhaseEnd

    rlPhaseStartTest "cpio -L - follow symbolic links"
        ln -s f1 f1_link
        rlRun "printf 'f1_link\n' | cpio -o > archive_sym.cpio 2>/dev/null" 0 "Create archive with symlink (without -L)"
        rlRun "printf 'f1_link\n' | cpio -oL > archive_follow.cpio 2>/dev/null" 0 "cpio -L follows symlinks"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd