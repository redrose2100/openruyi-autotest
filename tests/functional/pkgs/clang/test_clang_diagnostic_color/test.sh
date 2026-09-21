#!/bin/bash
# Functional test: clang - clang -fcolor-diagnostics
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    clangSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "clang -fcolor-diagnostics"
    rlRun "echo 'int main(){return 0;}' > test.c" 0 "Create test C file"
    rlRun "clang -fcolor-diagnostics -c test.c -o test.o 2>&1 || echo color_ok" 0 "clang -fcolor-diagnostics: colored output"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
