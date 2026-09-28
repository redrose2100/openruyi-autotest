#!/bin/bash
# Functional test: gcc - Preprocessor
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Preprocessor"
    rlRun "gcc -E macro.c -o macro.i" 0 "Preprocess with -E"
    rlRun "grep \"Hello Preprocessor\" macro.i" 0 "Verify macro expanded in preprocessed output"
    rlRun "gcc macro.i -o macro_bin" 0 "Compile preprocessed .i file"
    rlRun "./macro_bin" 0 "Run from preprocessed source"
    rlRun "gcc -DTEST_VAL=42 hello.c -o hello_def" 0 "Compile with -D flag"
    rlRun "./hello_def" 0 "Run with -D defined macro"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # gcc Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
