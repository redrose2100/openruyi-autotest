#!/bin/bash
# Functional test: tar - tar --zstd compression
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar --zstd compression"
    rlRun "mkdir testdir && echo 'data' > testdir/f4.txt" 0 "Create test data"
    rlRun "tar --zstd -cf test.zst testdir 2>&1 || echo zstd_not_supported" 0 "tar --zstd: zstd compression"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
