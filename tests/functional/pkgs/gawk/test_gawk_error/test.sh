#!/bin/bash
# Functional test: gawk - error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gawkSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "error handling"
    # An invalid option must make awk/gawk exit with a non-zero status and
    # print an error message.
    rlRun "awk --invalid-flag-xyz 2>&1" 2 "awk - error handling"
    rlRun "awk --invalid-flag-xyz 2>&1 | grep -qi 'invalid\\|unknown\\|unrecognized\\|usage'" 0 "awk - error message is printed"
    rlRun "gawk --invalid-flag-xyz 2>&1" 2 "gawk - error handling"
    rlRun "gawk --invalid-flag-xyz 2>&1 | grep -qi 'invalid\\|unknown\\|unrecognized\\|usage'" 0 "gawk - error message is printed"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # gawk Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
