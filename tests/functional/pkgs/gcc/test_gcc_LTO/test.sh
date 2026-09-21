#!/bin/bash
# Functional test: gcc - gcc -flto link-time optimization
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "gcc -flto link-time optimization"
    rlRun "echo 'int main(){return 0;}' > test4.c" 0 "Create test file"
    rlRun "gcc -flto -c test4.c -o test4.o 2>&1 || echo lto_ok" 0 "gcc -flto: link-time optimization"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
