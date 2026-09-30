#!/bin/bash

# Functional test: binutils - objdump

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



    rlPhaseStartTest "objdump"

    rlRun "objdump -f /usr/bin/ls 2>&1 | head -10" 0 "List files"

    rlRun "objdump -h /usr/bin/ls 2>&1 | head -20" 0 "List files"

    rlRun "objdump -d /usr/bin/ls 2>&1 | head -10" 0 "List files"

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

