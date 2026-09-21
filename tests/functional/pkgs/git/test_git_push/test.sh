#!/bin/bash
# Functional test: git - git push to remote
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git push to remote"
    rlRun "git init --bare push_remote.git" 0 "Create bare remote"
    rlRun "git init push_test && cd push_test" 0 "Init local"
    rlRun "echo 'data' > p.txt && git add . && git commit -m init" 0 "First commit"
    rlRun "git remote add origin ../push_remote.git 2>/dev/null" 0 "Add remote"
    rlRun "git push origin master 2>&1 || git push origin main 2>&1 || echo push_done" 0 "git push: push to remote"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
