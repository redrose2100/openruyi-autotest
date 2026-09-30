#!/bin/bash

# Functional test: sed - linesoperation

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    sedSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "linesoperation"

    rlRun "sed -n \"2p\" lines.txt" 0 "sed -n: printspecifylines"

    rlRun "sed \"2d\" lines.txt" 0 "sed d: deletespecifylines"

    rlRun "sed \"2a newline\" lines.txt" 0 "sed a: lines"

    rlRun "sed \"2i insertline\" lines.txt" 0 "sed i: lines"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # sed Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

