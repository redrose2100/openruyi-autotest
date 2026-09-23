#!/bin/bash
# Functional test: tmux - Options-and-settings
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

    rlPhaseStartTest "Options-and-settings"
    rlRun "tmux set-option -g status-interval 5 2>&1 " 0 "set-option -g: global"
    rlRun "tmux set-option -g -a status-left \"test\" 2>&1 || true" 0 "set-option -a: append"
    rlRun "tmux set-option -g mouse on 2>&1 " 0 "set-option: mouse on"
    rlRun "tmux set-option -s escape-time 10 2>&1 " 0 "set-option -s: server option"
    rlRun "tmux set-window-option -t testsess:win1 monitor-activity on 2>&1 " 0 "set-window-option: monitor activity"
    rlRun "tmux set-window-option -g automatic-rename on 2>&1 " 0 "set-window-option -g: global"
    rlRun "tmux show-options -g | head -10" 0 "show-options -g: global options"
    rlRun "tmux show-options -s | head -10" 0 "show-options -s: server options"
    rlRun "tmux show-window-options -t testsess:win1 | head -10" 0 "show-window-options: window options"
    rlRun "tmux show-window-options -g | head -10" 0 "show-window-options -g: global window options"
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
