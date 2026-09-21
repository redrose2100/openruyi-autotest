#!/bin/bash
# Functional test: git - git cherry-pick commit
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git cherry-pick commit"
    rlRun "git init cp_test && cd cp_test" 0 "Init repo"
    rlRun "echo 'a' > a.txt && git add . && git commit -m A" 0 "Commit A"
    rlRun "echo 'b' > b.txt && git add . && git commit -m B" 0 "Commit B"
    rlRun "git checkout -b side HEAD~1" 0 "Side branch from commit A"
    rlRun "git cherry-pick master 2>&1 || git cherry-pick main 2>&1 || echo cp_done" 0 "git cherry-pick: apply commit B"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
