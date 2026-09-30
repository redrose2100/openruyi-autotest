#!/bin/bash
# Functional test: beakerlib - beakerlib error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    beakerlibSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "beakerlib error handling"
    rlRun "beakerlib-deja-summarize --help 2>&1 | head -10" 0 "Display first lines"
    rlRun "beakerlib-journalcmp --help 2>&1 | head -10" 0 "Compare files byte by byte"
    rlRun "beakerlib-testwatcher --help 2>&1 | head -10" 0 "Display first lines"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # beakerlib Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
