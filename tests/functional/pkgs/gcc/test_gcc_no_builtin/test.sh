#!/bin/bash
# Functional test: gcc - gcc -fno-builtin disable builtins
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "gcc -fno-builtin disable builtins"
    rlRun "echo 'int main(){return 0;}' > test2.c" 0 "Create test file"
    rlRun "gcc -fno-builtin -c test2.c -o test2.o" 0 "gcc -fno-builtin: disable built-in functions"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
