#!/bin/bash
# Functional test: grep - Error-handling
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
    rlRun "mkdir subdir" 0 "Create subdir for directory test"
    rlPhaseEnd

    rlPhaseStartTest "Error-handling"
    rlRun "grep pattern nonexistent_file.txt 2>&1" 2 "Error on nonexistent file"
    rlRun "grep \"[\" test1.txt 2>&1" 2 "Error on invalid regex"
    rlRun "grep pattern subdir/ 2>&1" 2 "Error on directory without -r"
    rlRun "grep NONEXISTENT_PATTERN test1.txt" 1 "No match returns exit code 1"
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
