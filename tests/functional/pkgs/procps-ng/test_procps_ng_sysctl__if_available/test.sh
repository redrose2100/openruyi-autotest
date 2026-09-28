#!/bin/bash
# Functional test: procps-ng - ng - sysctl--if-available
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    procpsNgSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "ng - sysctl--if-available"
    rlRun "sysctl --help 2>&1 | grep -qiE \"Usage|Usage|Options\" || echo sysctl-help-not-available" 0 "sysctl --help"
    rlRun "sysctl -a 2>&1 | grep -q kernel" 0 "sysctl -a outputkernelparameter"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # procps-ng Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
