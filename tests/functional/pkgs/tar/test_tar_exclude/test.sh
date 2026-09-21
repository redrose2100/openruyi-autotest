#!/bin/bash
# Functional test: tar - tar --exclude patterns
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar --exclude patterns"
    rlRun "mkdir testdir && echo 'keep' > testdir/keep.txt && echo 'skip' > testdir/skip.log" 0 "Create test data"
    rlRun "tar -cf archive.tar --exclude='*.log' testdir" 0 "tar --exclude: exclude log files"
    rlRun "tar -tf archive.tar | grep -v 'skip.log' && tar -tf archive.tar | grep 'keep.txt'" 0 "tar --exclude: verify exclusion"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
