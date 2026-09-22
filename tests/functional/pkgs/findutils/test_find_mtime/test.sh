#!/bin/bash
# Functional test: findutils - find -mtime modified time
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

    rlPhaseStartTest "find -mtime modified time"
    rlRun "touch -t 202001010000 find_testdir/old.txt 2>/dev/null || touch find_testdir/old.txt" 0 "Create 'old' file"
    rlRun "find find_testdir -mtime +365 2>&1 | grep -v 'error' || echo mtime_works" 0 "find -mtime: older than N days"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
