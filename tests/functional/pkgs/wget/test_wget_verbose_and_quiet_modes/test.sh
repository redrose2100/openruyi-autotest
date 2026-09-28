#!/bin/bash
# Functional test: wget - Verbose-and-quiet-modes
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    wgetSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Verbose-and-quiet-modes"
    rlRun "wget --version -q 2>&1" 0 "wget -q quiet mode"
    rlRun "wget --version -v 2>&1" 0 "wget -v verbose mode"
    rlRun "wget --version -d 2>&1" 0 "wget -d debugmode"
    rlRun "wget --version --debug 2>&1" 0 "wget --debug debugmode"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # wget Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
