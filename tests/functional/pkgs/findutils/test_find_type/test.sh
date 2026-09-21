#!/bin/bash
# Functional test: findutils - find -type file/dir filter
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    findutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "find -type file/dir filter"
    rlRun "mkdir -p find_testdir/sub && touch find_testdir/f1.txt" 0 "Create find test structure"
    rlRun "find find_testdir -type d" 0 "find -type d: directories only"
    rlRun "find find_testdir -type f" 0 "find -type f: files only"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
