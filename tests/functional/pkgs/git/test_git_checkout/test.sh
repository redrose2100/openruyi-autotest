#!/bin/bash
# Functional test: git - git checkout switch branch
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git checkout switch branch"
    rlRun "git init co_test && cd co_test" 0 "Init repo"
    rlRun "echo 'main' > c.txt && git add . && git commit -m main" 0 "Main commit"
    rlRun "git checkout -b dev && echo 'dev' > d.txt && git add . && git commit -m dev" 0 "Dev branch"
    rlRun "git checkout master 2>/dev/null || git checkout main 2>/dev/null" 0 "git checkout: switch back"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
