#!/bin/bash

# Functional test: wget2 - Rate-limiting

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    wget2Setup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "Rate-limiting"

    rlRun "wget2 --limit-rate=100k --version 2>&1 | grep -q Wget" 0 "wget2 --limit-rate Option available"

    rlRun "wget2 --limit-rate=1M --version 2>&1 | grep -q Wget" 0 "wget2 --limit-rate supports M single"

    rlRun "wget2 --chunk-size=1M --version 2>&1 | grep -q Wget" 0 "wget2 --chunk-size multithreaddownloadoption"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # wget2 Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

