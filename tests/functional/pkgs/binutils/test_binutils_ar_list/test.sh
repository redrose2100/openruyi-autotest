#!/bin/bash
# Functional test: binutils - ar t list archive
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "ar t list archive"
    rlRun "echo 'int y;' > test7.c && gcc -c test7.c -o test7.o 2>/dev/null || touch test7.o" 0 "Create object"
    rlRun "ar cr libtest2.a test7.o 2>/dev/null || echo ar_cr_done" 0 "Create archive"
    rlRun "ar t libtest2.a" 0 "ar t: list archive contents"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
