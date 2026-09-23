#!/bin/bash
# Functional test: grep - File-listing---l---L
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    grepSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo -e 'Hello World\nHello Linux\nThis is a test\nHello everyone' > test1.txt" 0 "Create test1.txt"
    rlRun "echo -e 'No match here\nJust some text\nNothing to see' > test2.txt" 0 "Create test2.txt (no Hello)"
    rlPhaseEnd

    rlPhaseStartTest "File-listing---l---L"
    rlRun "grep -l Hello *.txt" 0 "List files with matches"
    rlRun "grep -L Hello *.txt" 0 "List files without matches"
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
