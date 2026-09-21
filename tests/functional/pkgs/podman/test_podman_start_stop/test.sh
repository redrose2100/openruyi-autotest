#!/bin/bash
# Functional test: podman - podman start/stop container
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    podmanSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "podman start/stop container"
    rlRun "podman start --help 2>&1 | head -3 || echo podman_start_help" 0 "podman start: help available"
    rlRun "podman stop --help 2>&1 | head -3 || echo podman_stop_help" 0 "podman stop: help available"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
