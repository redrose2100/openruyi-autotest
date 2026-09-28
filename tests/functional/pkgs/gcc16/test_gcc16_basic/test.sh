#!/bin/bash
# Functional test: gcc16 - gcc16 error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gcc16Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "gcc16 error handling"
    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"
    rlRun "cd $TmpDir" 0 "error handlingdirectory"
    rlRun "echo \"int main(){return 0;}\" > test.c" 0 "error handlingԴ"
    rlRun "gcc-16 -o test test.c" 0 "Condition test"
    rlRun "./test" 0 "Test operation"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # gcc16 Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
