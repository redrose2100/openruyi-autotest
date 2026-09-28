#!/bin/bash
# Functional test: vim - Vimdiff
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    echo "hello world" > file1.txt
    echo "hello ruyi" > file2.txt
    rlAssertExists "file1.txt"
    rlAssertExists "file2.txt"
    rlPhaseEnd

    rlPhaseStartTest "Vimdiff"
    rlRun "vimdiff -c 'qa!' file1.txt file2.txt 2>&1" 0 "vimdiff: compare files"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # vim Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
