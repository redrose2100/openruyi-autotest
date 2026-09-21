#!/bin/bash
# Functional test: tar - tar --diff verify archive
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar --diff verify archive"
    rlRun "mkdir testdir && echo 'data' > testdir/f5.txt" 0 "Create test data"
    rlRun "tar -cf archive.tar testdir" 0 "create archive"
    rlRun "tar --diff -f archive.tar testdir/f5.txt" 0 "tar --diff: verify file unchanged"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
