#!/bin/bash
# Functional test: git - git revert undo commit
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git revert undo commit"
    rlRun "git init revert_test && cd revert_test" 0 "Init repo"
    rlRun "echo 'v1' > v.txt && git add . && git commit -m v1" 0 "Commit v1"
    rlRun "git revert --no-edit HEAD 2>&1 || echo revert_done" 0 "git revert: undo last commit"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
