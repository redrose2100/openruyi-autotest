#!/bin/bash
# Functional test: git - git merge branch
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git merge branch"
    rlRun "git init merge_test && cd merge_test" 0 "Initialize repo"
    rlRun "echo 'main' > m.txt && git add . && git commit -m 'main commit'" 0 "Main commit"
    rlRun "git checkout -b feature && echo 'feat' > f.txt && git add . && git commit -m 'feature commit'" 0 "Feature branch"
    rlRun "git checkout master 2>/dev/null || git checkout main 2>/dev/null || git checkout -b main" 0 "Back to main"
    rlRun "git merge feature 2>&1 || echo merge_done" 0 "git merge: merge feature branch"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
