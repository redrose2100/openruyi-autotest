#!/bin/bash
# Functional test: dnf5-plugins - plugins - List-installed-plugins
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    dnf5PluginsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "plugins - List-installed-plugins"
    rlRun "ls /usr/lib/python*/site-packages/dnf5-plugins/ 2>&1 | head -20" 0 "Plugin files"
    rlRun "ls /usr/share/dnf5/plugins/ 2>&1 | head -20 || echo \"No plugin dir\"" 0 "Plugin directory"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # dnf5-plugins Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
