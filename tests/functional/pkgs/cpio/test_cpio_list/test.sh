#!/bin/bash
# Functional test: cpio - cpio list archive
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cpioSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "cpio list archive"
    rlRun "echo 'file1' > f1 && echo f1 | cpio -o > a.cpio 2>/dev/null" 0 "Create archive"
    rlRun "cpio -t < a.cpio 2>&1 | head -5" 0 "cpio -t: list archive"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
