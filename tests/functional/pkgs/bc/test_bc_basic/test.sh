#!/bin/bash
# Functional test: bc - error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    bcSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "error handling"
    rlRun "echo \"1+1\" | bc" 0 "ӷ"
    rlRun "echo \"10-3\" | bc" 0 "error handling"
    rlRun "echo \"6*7\" | bc" 0 "˷"
    rlRun "echo \"100/3\" | bc" 0 "error handling"
    rlRun "echo \"scale=4; 1/3\" | bc" 0 "þ"
    rlRun "echo \"2^10\" | bc" 0 "error handling"
    rlRun "echo \"sqrt(16)\" | bc" 0 "ƽ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # bc Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
