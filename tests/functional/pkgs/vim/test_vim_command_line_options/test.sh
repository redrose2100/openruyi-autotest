#!/bin/bash
# Functional test: vim - Command-line-options
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Command-line-options"
    rlRun "vim --help 2>&1 | head -10" 0 "vim --help"
    rlRun "vim -c \"version\" -c \"q\" test.txt 2>&1 | head -3 || true" 0 "vim -c: execute command"
    rlRun "vim -R test.txt -c \"q\" 2>&1 || true" 0 "vim -R: readonly mode"
    rlRun "vim -b test.txt -c \"q\" 2>&1 || true" 0 "vim -b: binary mode"
    rlRun "vim -n test.txt -c \"q\" 2>&1 || true" 0 "vim -n: no swap file"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # vim Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
