#!/bin/bash
# Functional test: gcc - Multi-file-compilation
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

    rlPhaseStartTest "Multi-file-compilation"
    rlRun "gcc -c add.c -o add.o" 0 "Compile add.c to object"
    rlRun "gcc -c main.c -o main.o" 0 "Compile main.c to object"
    rlRun "gcc add.o main.o -o multi_bin" 0 "Link multiple objects"
    rlRun "./multi_bin" 0 "Run multi-file program"
    rlRun "gcc add.c main.c -o multi_bin2" 0 "Compile multiple files in one command"
    rlRun "./multi_bin2" 0 "Run single-command multi-file program"
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
