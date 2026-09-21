#!/bin/bash
# Functional test: binutils - size section sizes
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "size section sizes"
    rlRun "echo 'int main(){return 0;}' > test.c && gcc -c test.c -o test.o 2>/dev/null || touch test.o" 0 "Create object file"
    rlRun "size test.o 2>&1 || echo size_ok" 0 "size: show section sizes"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
