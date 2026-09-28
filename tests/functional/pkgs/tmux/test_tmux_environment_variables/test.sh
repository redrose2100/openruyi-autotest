#!/bin/bash
# Functional test: tmux - Environment-variables
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tmuxSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Environment-variables"
    rlRun "tmux set-environment -g MY_VAR test_value" 0 "set-environment -g: global env"
    rlRun "tmux set-environment -t testsess SESSION_VAR session_val" 0 "set-environment: session env"
    rlRun "tmux set-environment -gru MY_VAR" 0 "set-environment -gur: update then remove"
    rlRun "tmux show-environment -g | head -10" 0 "show-environment -g: global env"
    rlRun "tmux show-environment -t testsess | head -10" 0 "show-environment: session env"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # tmux Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
