#!/bin/bash
# Functional test: tmux - Messages-and-display
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

    rlPhaseStartTest "Messages-and-display"
    rlRun "tmux display-message \"test message\" 2>&1 || true" 0 "display-message: show message"
    rlRun "tmux display-message -p \"session: #{session_name}\"" 0 "display-message -p: print format"
    rlRun "tmux show-messages 2>&1 " 0 "show-messages: message log"
    rlRun "tmux display-popup -C 2>&1 " 0 "display-popup -C: close popup"
    rlRun "tmux clear-history -t testsess:win1" 0 "clear-history: clear pane history"
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
