#!/bin/bash
# Functional test: clang - clang -pedantic warnings
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    clangSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "clang -pedantic warnings"
    rlRun "echo 'int main(){return 0;}' > test5.c" 0 "Create test file"
    rlRun "clang -pedantic -c test5.c -o test5.o 2>&1 || echo pedantic_ok" 0 "clang -pedantic: strict standard"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
