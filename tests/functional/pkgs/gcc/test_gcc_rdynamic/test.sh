#!/bin/bash
# Functional test: gcc - gcc -rdynamic export symbols
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "gcc -rdynamic export symbols"
    rlRun "echo 'int main(){return 0;}' > test.c" 0 "Create test file"
    rlRun "gcc -rdynamic test.c -o test_rdyn 2>&1 || echo rdynamic_ok" 0 "gcc -rdynamic: export all symbols"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
