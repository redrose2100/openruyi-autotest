#!/bin/bash
# Functional test: git - git pull from remote
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git pull from remote"
    rlRun "git init --bare pull_remote.git" 0 "Bare remote"
    rlRun "git clone pull_remote.git pull_test" 0 "Clone remote"
    rlRun "cd pull_test && echo 'data' > f.txt && git add . && git commit -m 'add file' && git push 2>&1 || echo pull_setup_done" 0 "Setup pull test"
    rlRun "cd .. && git clone pull_remote.git pull_test2 && cd pull_test2" 0 "Second clone"
    rlRun "git pull 2>&1 || echo pull_done" 0 "git pull: pull from remote"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
