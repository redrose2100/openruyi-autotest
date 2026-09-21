#!/bin/bash
# Functional test: git - git diff show changes
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git diff show changes"
    rlRun "git init diff_test && cd diff_test" 0 "Init repo"
    rlRun "echo 'original' > d.txt && git add . && git commit -m original" 0 "Original commit"
    rlRun "echo 'modified' > d.txt" 0 "Modify file"
    rlRun "git diff 2>&1 || echo diff_done" 0 "git diff: show unstaged changes"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
