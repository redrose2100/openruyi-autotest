#!/bin/bash
# Functional test: lz4 - error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    lz4Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "error handling"
    rlRun "lz4 --invalid-flag-xyz 2>&1 " 0 " lz4 Чerror handling"
    rlRun "lz4c --invalid-flag-xyz 2>&1 " 0 " lz4c Чerror handling"
    rlRun "lz4cat --invalid-flag-xyz 2>&1 " 0 " lz4cat Чerror handling"
    rlRun "unlz4 --invalid-flag-xyz 2>&1 " 0 " unlz4 Чerror handling"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # lz4 Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
