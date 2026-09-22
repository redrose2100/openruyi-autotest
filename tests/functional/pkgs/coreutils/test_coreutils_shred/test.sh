#!/bin/bash
# Functional test: coreutils - shred secure file removal
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"


    rlPhaseEnd

    rlPhaseStartTest "shred secure file removal"
    rlRun "echo \"secret data\" > shred_test.txt" 0 "Create file to shred"
    rlRun "shred -n 1 -u shred_test.txt" 0 "shred remove file securely"
    rlRun "test ! -f shred_test.txt" 0 "shred: file removed"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
