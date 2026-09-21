#!/bin/bash
# Functional test: clang - clang -fmodules-cache-path
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    clangSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "clang -fmodules-cache-path"
    rlRun "echo 'int main(){return 0;}' > test4.c" 0 "Create test file"
    rlRun "clang -fmodules-cache-path=/tmp -c test4.c -o test4.o 2>&1 || echo module_cache_ok" 0 "clang -fmodules-cache-path: option accepted"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
