#!/bin/bash
# Functional test: tar - tar --transform rename
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar --transform rename"
    rlRun "mkdir testdir && echo 'data' > testdir/f6.txt" 0 "Create test data"
    rlRun "tar -cf archive.tar --transform='s/testdir/newdir/' testdir" 0 "tar --transform: rename paths"
    rlRun "tar -tf archive.tar | grep newdir" 0 "tar --transform: verify rename"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
