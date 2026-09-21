#!/bin/bash
# Functional test: gcc - gcc -fstack-protector
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "gcc -fstack-protector"
    rlRun "echo 'int main(){return 0;}' > test3.c" 0 "Create test file"
    rlRun "gcc -fstack-protector -c test3.c -o test3.o" 0 "gcc -fstack-protector: stack protection"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
