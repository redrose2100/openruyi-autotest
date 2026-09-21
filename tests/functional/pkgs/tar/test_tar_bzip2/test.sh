#!/bin/bash
# Functional test: tar - tar -j bzip2 compression
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar -j bzip2 compression"
    rlRun "mkdir testdir && echo 'data' > testdir/f3.txt" 0 "Create test data"
    rlRun "tar -cjf test.bz2 testdir" 0 "tar -cjf: bzip2 compressed archive"
    rlRun "test -f test.bz2" 0 "tar -cjf: archive created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
