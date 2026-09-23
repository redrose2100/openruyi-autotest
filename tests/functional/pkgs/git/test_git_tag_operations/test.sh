#!/bin/bash
# Functional test: git - Tag-operations
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gitSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "git init" 0 "Initialize git repository"
    rlRun "echo test > file.txt" 0 "Create test file"
    rlRun "git add file.txt" 0 "Stage test file"
    rlRun "git commit -m initial" 0 "Create initial commit"
    rlPhaseEnd

    rlPhaseStartTest "Tag-operations"
    rlRun "git tag v1.0" 0 "git tag: create tag"
    rlRun "git tag" 0 "git tag: list tags"
    rlRun "git tag -d v1.0" 0 "git tag -d: delete tag"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # git Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
