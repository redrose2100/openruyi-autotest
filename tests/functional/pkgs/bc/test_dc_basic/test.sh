#!/bin/bash

# Functional test: bc -error handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    bcSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "error handling"

    rlRun "echo \"1 1 + p\" | dc" 0 "dc ӷ"

    rlRun "echo \"10 3 - p\" | dc" 0 "dc "

    rlRun "echo \"6 7 * p\" | dc" 0 "dc ˷"

    rlRun "echo \"100 3 / p\" | dc" 0 "dc "

    rlRun "echo \"4 k 1 3 / p\" | dc" 0 "dc error handling"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # bc Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

