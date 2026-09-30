#!/bin/bash

# Functional test: binutils - ar

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    binutilsSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "ar"

    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"

    rlRun "cd $TmpDir" 0 "error handlingdirectory"

    rlRun "echo \"test\" > file1.txt" 0 "ļ1"

    rlRun "echo \"data\" > file2.txt" 0 "ļ2"

    rlRun "ar cr test.a file1.txt file2.txt" 0 "Create static library archive"

    rlRun "test -f test.a" 0 "Test operation"

    rlRun "ar t test.a" 0 "List archive contents"

    rlRun "ar x test.a" 0 "Archive operation"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # binutils Package managed by lib.sh 's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

