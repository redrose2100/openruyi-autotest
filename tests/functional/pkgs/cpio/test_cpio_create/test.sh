#!/bin/bash
# Functional test: cpio - cpio create archive
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cpioSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "cpio create archive"
    rlRun "echo 'file1' > f1 && echo 'file2' > f2" 0 "Create files"
    rlRun "printf 'f1\nf2\n' | cpio -o > archive.cpio 2>/dev/null && test -f archive.cpio" 0 "cpio: create archive"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
