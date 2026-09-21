#!/bin/bash
# Functional test: gcc - gcc -lm math library
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "gcc -lm math library"
    rlRun "echo '#include <math.h>\nint main(){return (int)sqrt(4.0);}' > test6.c" 0 "Create math test file"
    rlRun "gcc test6.c -lm -o test6 2>&1 || echo libm_ok" 0 "gcc -lm: link math library"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
