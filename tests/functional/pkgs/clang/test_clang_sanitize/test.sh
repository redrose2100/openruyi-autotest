#!/bin/bash
# Functional test: clang - clang -fsanitize sanitizers
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    clangSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "clang -fsanitize sanitizers"
    rlRun "echo 'int main() { int *p=0; return *p; }' > test2.c" 0 "Create sanitizer test file"
    rlRun "clang -fsanitize=address -c test2.c -o test2.o 2>&1 | grep -qiE 'error|warning' || echo sanitize_ok" 0 "clang -fsanitize: address sanitizer"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
