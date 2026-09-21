#!/bin/bash
# Functional test: bc - bc -l math library
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    bcSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "bc -l math library"
    rlRun "echo 's(3.14159/2)' | bc -l 2>&1 | head -1" 0 "bc -l: math library"
    rlRun "echo 'e(1)' | bc -l 2>&1 | head -1" 0 "bc -l: exponential"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
