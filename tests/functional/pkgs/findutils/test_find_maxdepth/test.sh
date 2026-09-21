#!/bin/bash
# Functional test: findutils - find -maxdepth limit depth
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    findutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "find -maxdepth limit depth"
    rlRun "mkdir -p find_testdir/l1/l2/l3 && touch find_testdir/l1/l2/l3/deep.txt" 0 "Create nested dirs"
    rlRun "find find_testdir -maxdepth 2" 0 "find -maxdepth 2: limit to 2 levels"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
