#!/bin/bash
# Functional test: coreutils - join merge on common field
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo -e '1 a\n2 b\n3 c' > sorted1.txt && echo -e '1 x\n2 y\n4 z' > sorted2.txt" 0 "Create join input files"

    rlPhaseEnd

    rlPhaseStartTest "join merge on common field"
    rlRun "join sorted1.txt sorted2.txt 2>&1" 0 "join merge files"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
