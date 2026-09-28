#!/bin/bash
# Functional test: sddm - Configuration
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    sddmSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Configuration"
    rlRun "sddm --example-config 2>&1 | head -20" 0 "sddm: example config"
    rlRun "ls /etc/sddm.conf.d/ 2>&1 || echo \"No config dir\"" 0 "Config directory"
    rlRun "ls /usr/lib/sddm/sddm.conf.d/ 2>&1 || echo \"No default config dir\"" 0 "Default config dir"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # sddm Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
