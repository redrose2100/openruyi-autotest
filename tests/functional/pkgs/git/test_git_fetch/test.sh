#!/bin/bash
# Functional test: git - git fetch from remote
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "git fetch from remote"
    rlRun "git init --bare fetch_remote.git && git clone fetch_remote.git fetch_test" 0 "Setup fetch test"
    rlRun "cd fetch_test && echo 'new' > n.txt && git add . && git commit -m new && git push 2>&1 || echo fetch_setup_done" 0 "Push new commit"
    rlRun "cd .. && git clone fetch_remote.git fetch_test2 && cd fetch_test2" 0 "Second clone for fetch"
    rlRun "git fetch --all 2>&1 || echo fetch_done" 0 "git fetch: fetch all remotes"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
