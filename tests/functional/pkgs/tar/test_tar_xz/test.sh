#!/bin/bash
# Functional test: tar - tar -J xz compression
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar -J xz compression"
    rlRun "mkdir testdir && echo 'data' > testdir/f2.txt" 0 "Create test data"
    rlRun "tar -cJf test.xz testdir" 0 "tar -cJf: xz compressed archive"
    rlRun "test -f test.xz" 0 "tar -cJf: archive created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
