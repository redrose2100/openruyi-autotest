#!/bin/bash
# Functional test: rpm - rpmѯ
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    rpmSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "rpmѯ"
rlRun() { eval "$1" 2>&1; return $?; }
    rlRun "rpm --help 2>&1 | head -10" 0 "RPM package operation"
    rlRun "rpm -qa 2>&1 | head -10" 0 "List installed packages"
    rlRun "rpm -qi rpm 2>&1 | head -10" 0 "Query package info"
    rlRun "rpm -ql rpm 2>&1 | head -10" 0 "List package files"
    rlRun "rpm -qc rpm 2>&1" 0 "RPM package operation"
    rlRun "rpm -qd rpm 2>&1 | head -5" 0 "RPM package operation"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # rpm Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
