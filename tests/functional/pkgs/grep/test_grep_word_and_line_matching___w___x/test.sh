#!/bin/bash
# Functional test: grep - Word-and-line-matching---w---x
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    grepSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Word-and-line-matching---w---x"
    rlRun "echo \"helloworld\" > word_test.txt" 0 "Create word test file"
    rlRun "echo \"hello world\" >> word_test.txt" 0 "Add line with separate words"
    rlRun "test $(grep -w hello word_test.txt | wc -l) -eq 1" 0 "Whole word match: hello matches only standalone"
    rlRun "echo \"exact match\" > line_test.txt" 0 "Create line test file"
    rlRun "echo \"not exact match here\" >> line_test.txt" 0 "Add different line"
    rlRun "test $(grep -x \"exact match\" line_test.txt | wc -l) -eq 1" 0 "Whole line exact match"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # grep Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
