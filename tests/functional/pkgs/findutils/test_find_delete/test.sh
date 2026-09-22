#!/bin/bash
# Functional test: findutils - find -delete remove files
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

    rlPhaseStartTest "find -delete remove files"
    rlRun "touch find_testdir/todel.txt" 0 "Create file to delete"
    rlRun "find find_testdir -name 'todel.txt' -delete" 0 "find -delete: remove matching files"
    rlRun "test ! -f find_testdir/todel.txt" 0 "find -delete: file removed"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
