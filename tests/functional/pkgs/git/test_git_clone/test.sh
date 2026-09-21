#!/bin/bash
# Functional test: git - git clone repository
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git clone repository"
    rlRun "mkdir testrepo && cd testrepo && git init && echo 'hello' > README.md && git add . && git commit -m init" 0 "Create test repo"
    rlRun "cd .. && git clone testrepo cloned" 0 "git clone: clone local repo"
    rlRun "test -d cloned/.git" 0 "git clone: .git directory created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
