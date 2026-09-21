#!/bin/bash
# Functional test: tar - tar -z gzip compression
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar -z gzip compression"
    rlRun "mkdir testdir && echo 'data' > testdir/f1.txt" 0 "Create test data"
    rlRun "tar -czf test.tgz testdir" 0 "tar -czf: gzip compressed archive"
    rlRun "tar -tzf test.tgz" 0 "tar -tzf: list gzip archive"
    rlRun "test -f test.tgz" 0 "tar -czf: archive created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
