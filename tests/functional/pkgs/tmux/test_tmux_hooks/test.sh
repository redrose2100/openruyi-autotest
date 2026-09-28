#!/bin/bash
# Functional test: tmux - Hooks
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

    rlPhaseStartTest "Hooks"
    rlRun "tmux set-hook -g session-created \"display-message created\"" 0 "set-hook: session-created"
    rlRun "tmux set-hook -g client-attached \"display-message attached\"" 0 "set-hook: client-attached"
    rlRun "tmux show-hooks -g" 0 "show-hooks -g: global hooks"
    rlRun "tmux set-hook -gu session-created" 0 "set-hook -gu: remove global hook"
    rlRun "tmux set-hook -gu client-attached" 0 "set-hook -gu: remove hook"
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
