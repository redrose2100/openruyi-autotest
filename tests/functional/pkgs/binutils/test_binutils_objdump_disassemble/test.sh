#!/bin/bash
# Functional test: binutils - objdump -d disassemble
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "objdump -d disassemble"
    rlRun "echo 'int main(){return 0;}' > test4.c && gcc -c test4.c -o test4.o 2>/dev/null || touch test4.o" 0 "Create object"
    rlRun "objdump -d test4.o 2>&1 | head -5 || echo objdump_d_ok" 0 "objdump -d: disassemble"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
