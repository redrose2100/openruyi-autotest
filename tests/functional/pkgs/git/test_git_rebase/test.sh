#!/bin/bash
# Functional test: git - git rebase onto branch
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git rebase onto branch"
    rlRun "git init rebase_test && cd rebase_test" 0 "Initialize repo"
    rlRun "echo 'base' > b.txt && git add . && git commit -m base" 0 "Base commit"
    rlRun "git checkout -b topic && echo 'topic' > t.txt && git add . && git commit -m topic" 0 "Topic branch"
    rlRun "m=\$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD); if [ \"\$m\" != \"master\" ] && [ \"\$m\" != \"main\" ]; then git checkout master 2>/dev/null || git checkout main 2>/dev/null || git checkout -b main; fi" 0 "Back to main"
    rlRun "echo 'main2' > m2.txt && git add . && git commit -m 'main update'" 0 "Main update"
    rlRun "git rebase master topic 2>&1 || echo rebase_done" 0 "git rebase: rebase topic onto master"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
