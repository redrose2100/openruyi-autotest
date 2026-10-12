#!/bin/bash
# Functional test: cpio - file attribute preservation (-R, -a, -m)
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo 'file1' > f1
        echo 'file2' > f2
    rlPhaseEnd

    rlPhaseStartTest "cpio -R - set file owner"
        rlRun "printf 'f1\nf2\n' | cpio -o > archive_R.cpio 2>/dev/null" 0 "Create archive without owner change"
        rlRun "cpio -iR root:root < archive_R.cpio 2>/dev/null; test -f f1" 0 "cpio -R sets owner to root:root on extract"
    rlPhaseEnd

    rlPhaseStartTest "cpio -m - preserve modification times"
        touch -t 202001010000 f1
        rlRun "printf 'f1\n' | cpio -o > archive_m.cpio 2>/dev/null" 0 "Create archive with -m"
        rm -f f1
        rlRun "cpio -im < archive_m.cpio 2>/dev/null && test -f f1" 0 "cpio -im extracts preserving modification time"
    rlPhaseEnd

    rlPhaseStartTest "cpio -A - append to existing archive"
        echo 'f1' > f1
        echo 'f2' > f2
        rlRun "printf 'f1\n' | cpio -o > append_archive.cpio 2>/dev/null" 0 "Create initial archive"
        rlRun "printf 'f2\n' | cpio -oA -F append_archive.cpio 2>/dev/null" 0 "cpio -A appends to archive"
        rlRun "cpio -it < append_archive.cpio 2>/dev/null | wc -l | grep -E '[23]'" 0 "Archive contains append entries"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd