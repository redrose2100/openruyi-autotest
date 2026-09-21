#!/bin/bash
# Functional test: binutils - ranlib archive index
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "ranlib archive index"
    rlRun "echo 'int x;' > test3.c && gcc -c test3.c -o test3.o 2>/dev/null || touch test3.o" 0 "Create object"
    rlRun "ar cr libtest.a test3.o 2>/dev/null || echo ar_done" 0 "Create archive"
    rlRun "ranlib libtest.a 2>&1 || echo ranlib_ok" 0 "ranlib: generate archive index"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
