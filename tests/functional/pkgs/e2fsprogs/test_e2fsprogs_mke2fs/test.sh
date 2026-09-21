#!/bin/bash
# Functional test: e2fsprogs - mke2fs create filesystem
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    e2fsprogsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "mke2fs create filesystem"
    rlRun "dd if=/dev/zero of=test.img bs=1M count=10 2>/dev/null" 0 "Create image file"
    rlRun "mke2fs -F test.img 2>&1 | head -5" 0 "mke2fs: create ext2 filesystem"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
