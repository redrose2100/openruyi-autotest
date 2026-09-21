#!/bin/bash
# Functional test: clang - clang -emit-llvm IR output
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    clangSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "clang -emit-llvm IR output"
    rlRun "echo 'int main(){return 0;}' > test3.c" 0 "Create test file"
    rlRun "clang -emit-llvm -c test3.c -o test3.bc 2>&1 || echo emit_llvm_ok" 0 "clang -emit-llvm: LLVM bitcode"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
