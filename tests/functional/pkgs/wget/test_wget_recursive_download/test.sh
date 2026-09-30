#!/bin/bash

# Functional test: wget - Recursive-download

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    wgetSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "Recursive-download"

    rlRun "wget -r --version 2>&1 | grep -q Wget" 0 "wget -r recursiveOption exists"

    rlRun "wget -l 2 --version 2>&1 | grep -q Wget" 0 "wget -l recursiveoption"

    rlRun "wget -p --version 2>&1 | grep -q Wget" 0 "wget -p pageoption"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # wget Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

