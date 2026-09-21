#!/bin/bash
# Functional test: coreutils - rmdir remove empty directory
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"


    rlPhaseEnd

    rlPhaseStartTest "rmdir remove empty directory"
    rlRun "mkdir rmdir_test" 0 "Create empty directory"
    rlRun "rmdir rmdir_test" 0 "rmdir remove empty directory"
    rlRun "test ! -d rmdir_test" 0 "rmdir: directory removed"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
