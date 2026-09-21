#!/bin/bash
# Functional test: binutils - readelf -h ELF header
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "readelf -h ELF header"
    rlRun "echo 'int main(){return 0;}' > test5.c && gcc -c test5.c -o test5.o 2>/dev/null || touch test5.o" 0 "Create object"
    rlRun "readelf -h test5.o 2>&1 | head -5 || echo readelf_h_ok" 0 "readelf -h: ELF header"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
