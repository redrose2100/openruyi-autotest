#!/bin/bash
# Functional test: e2fsprogs - dumpe2fs filesystem info
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    e2fsprogsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "dumpe2fs filesystem info"
    rlRun "dd if=/dev/zero of=test2.img bs=1M count=10 2>/dev/null" 0 "Create image"
    rlRun "mke2fs -F test2.img 2>/dev/null" 0 "Format"
    rlRun "dumpe2fs test2.img 2>&1 | head -10" 0 "dumpe2fs: filesystem info"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
