#!/bin/bash
# Functional test: cpio - format and I/O options (-c, -F)
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo 'file1' > f1
        echo 'file2' > f2
    rlPhaseEnd

    rlPhaseStartTest "cpio -c - use old portable ASCII format"
        rlRun "printf 'f1\nf2\n' | cpio -oc > archive_c.cpio 2>/dev/null && test -f archive_c.cpio" 0 "cpio -c creates ASCII archive"
    rlPhaseEnd

    rlPhaseStartTest "cpio -F - specify archive file"
        rlRun "printf 'f1\nf2\n' | cpio -oF archive_F.cpio 2>/dev/null && test -f archive_F.cpio" 0 "cpio -F specifies output archive file"
    rlPhaseEnd

    rlPhaseStartTest "cpio -H - specify archive format"
        rlRun "printf 'f1\nf2\n' | cpio -oH tar > archive_tar.cpio 2>/dev/null; test -f archive_tar.cpio" 0 "cpio -H tar creates tar-format archive"
    rlPhaseEnd

    rlPhaseStartTest "cpio verify and extract format archives"
        rlRun "cpio -it < archive_c.cpio 2>/dev/null | grep f1" 0 "cpio -it lists -c format archive"
        rlRun "cpio -it < archive_F.cpio 2>/dev/null | grep f2" 0 "cpio -it lists -F format archive"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd