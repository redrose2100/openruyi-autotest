#!/bin/bash
# Functional test: gcc - Special-features
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

    rlPhaseStartTest "Special-features"
    rlRun "gcc -std=c99 hello.c -o hello_c99" 0 "Compile with C99 standard"
    rlRun "gcc attr.c -o attr_test" 0 "Compile with __attribute__"
    rlRun "./attr_test" 0 "Run attribute test"
    rlRun "gcc -I include_dir main.c include_dir/mylib.c -o include_test" 0 "Compile with -I include path"
    rlRun "./include_test" 0 "Run include path test"
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
