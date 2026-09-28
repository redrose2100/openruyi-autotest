#!/bin/bash
# Functional test: make - Options
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    makeSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Options"
    rlRun "make -n" 0 "make -n: dry run"
    rlRun "make -B" 0 "make -B: always make"
    rlRun "make --just-print" 0 "make --just-print"
    rlRun "make -d 2>&1 | head -5" 0 "make -d: debug output"
    rlRun "make --debug=b 2>&1 | head -5" 0 "make --debug=b: basic debug"
    rlRun "make -q" 0 "make -q: question mode"
    rlRun "make -s" 0 "make -s: silent"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # make Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
