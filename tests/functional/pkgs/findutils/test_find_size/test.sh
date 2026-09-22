#!/bin/bash
# Functional test: findutils - find -size filter by size
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    findutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "mkdir -p find_testdir" 0 "Create test directory"

    rlPhaseEnd

    rlPhaseStartTest "find -size filter by size"
    rlRun "dd if=/dev/zero of=find_testdir/big.txt bs=1024 count=100 2>/dev/null" 0 "Create 100KB file"
    rlRun "dd if=/dev/zero of=find_testdir/small.txt bs=1 count=10 2>/dev/null" 0 "Create 10B file"
    rlRun "find find_testdir -size +50k" 0 "find -size +50k: larger than 50KB"
    rlRun "find find_testdir -size -1k" 0 "find -size -1k: smaller than 1KB"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
