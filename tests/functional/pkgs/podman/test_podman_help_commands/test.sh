#!/bin/bash
# Functional test: podman - Help-commands
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    podmanSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Help-commands"
    rlRun "podman manifest --help 2>&1 | head -5" 0 "podman manifest help"
    rlRun "podman healthcheck --help 2>&1 | head -5" 0 "podman healthcheck help"
    rlRun "podman events --help 2>&1 | head -5" 0 "podman events help"
    rlRun "podman pod list 2>&1 | head -5" 0 "podman pod list"
    rlRun "podman-remote --help 2>&1 | head -5" 0 "podman-remote help"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # podman Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
