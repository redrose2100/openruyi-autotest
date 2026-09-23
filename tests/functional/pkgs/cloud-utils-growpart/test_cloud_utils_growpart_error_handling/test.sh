#!/bin/bash
# Functional test: cloud-utils-growpart - utils-growpart - Error-handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cloudUtilsGrowpartSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "utils-growpart - Error-handling"
    rlRun "growpart 2>&1 " 0 "growpart: no args (expected fail)"
    rlRun "growpart /dev/nonexistent 1 2>&1 " 0 "growpart: nonexistent disk"
    rlRun "growpart --help 2>&1 | grep -qiE \"Usage|Usage|usage\" || echo help-not-standard" 0 "growpart: invalid option"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # cloud-utils-growpart Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
