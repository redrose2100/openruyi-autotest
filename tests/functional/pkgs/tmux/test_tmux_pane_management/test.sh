#!/bin/bash
# Functional test: tmux - Pane-management
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

    rlPhaseStartTest "Pane-management"
    rlRun "tmux split-window -t testsess:win1" 0 "split-window: horizontal split"
    rlRun "tmux split-window -h -t testsess:win1" 0 "split-window -h: vertical split"
    rlRun "tmux split-window -v -t testsess:win1" 0 "split-window -v: vertical explicit"
    rlRun "tmux split-window -t testsess:win1 -l 10" 0 "split-window -l: with size"
    rlRun "tmux split-window -t testsess:win1 -d" 0 "split-window -d: don't focus"
    rlRun "tmux split-window -t testsess:win1 -f" 0 "split-window -f: full size"
    rlRun "tmux split-window -t testsess:win1 -b" 0 "split-window -b: before"
    rlRun "tmux split-window -t testsess:win1 -I" 0 "split-window -I: create empty pane"
    rlRun "tmux list-panes -t testsess:win1" 0 "list-panes: list panes"
    rlRun "tmux list-panes -as" 0 "list-panes -as: all panes"
    rlRun "tmux list-panes -t testsess:win1 -F \"#{pane_id}\"" 0 "list-panes -F: formatted"
    rlRun "tmux display-panes -t testsess 2>&1 " 0 "display-panes: show pane IDs"
    rlRun "tmux select-pane -t testsess:win1.0" 0 "select-pane: by ID"
    rlRun "tmux select-pane -l -t testsess:win1" 0 "select-pane -l: last pane"
    rlRun "tmux select-pane -U -t testsess:win1" 0 "select-pane -U: up"
    rlRun "tmux select-pane -D -t testsess:win1" 0 "select-pane -D: down"
    rlRun "tmux select-pane -L -t testsess:win1" 0 "select-pane -L: left"
    rlRun "tmux select-pane -R -t testsess:win1" 0 "select-pane -R: right"
    rlRun "tmux resize-pane -t testsess:win1.0 -y 15 2>&1 " 0 "resize-pane -y: height"
    rlRun "tmux resize-pane -t testsess:win1.0 -x 80 2>&1 " 0 "resize-pane -x: width"
    rlRun "tmux resize-pane -t testsess:win1.0 -U 2>&1 " 0 "resize-pane -U: up"
    rlRun "tmux resize-pane -t testsess:win1.0 -D 2>&1 " 0 "resize-pane -D: down"
    rlRun "tmux resize-pane -t testsess:win1.0 -L 2>&1 " 0 "resize-pane -L: left"
    rlRun "tmux resize-pane -t testsess:win1.0 -R 2>&1 " 0 "resize-pane -R: right"
    rlRun "tmux resize-pane -Z -t testsess:win1.0 2>&1 " 0 "resize-pane -Z: zoom"
    rlRun "tmux break-pane -t testsess:win1.1 -d -n broken_pane" 0 "break-pane -d: break pane to new window"
    rlRun "tmux join-pane -s testsess:broken_pane.0 -t testsess:win1 2>&1 " 0 "join-pane: join pane back"
    rlRun "tmux move-pane -t testsess:win2 2>&1 " 0 "move-pane: move pane"
    rlRun "tmux swap-pane -s testsess:win1.0 -t testsess:win1.1 2>&1 " 0 "swap-pane: swap panes"
    rlRun "tmux last-pane -t testsess:win1" 0 "last-pane: switch to last pane"
    rlRun "tmux split-window -t testsess:win1" 0 "kill-pane: create temp pane"
    rlRun "tmux kill-pane -t testsess:win1.1 2>&1 " 0 "kill-pane: kill pane"
    rlRun "tmux kill-pane -a -t testsess:win1 2>&1 " 0 "kill-pane -a: kill all but current"
    rlRun "tmux capture-pane -t testsess:win1 -p" 0 "capture-pane -p: print to stdout"
    rlRun "tmux capture-pane -t testsess:win1 -S -10 -E -1 -p 2>&1 " 0 "capture-pane: range capture"
    rlRun "tmux capture-pane -t testsess:win1 -J -p 2>&1 " 0 "capture-pane -J: join lines"
    rlRun "tmux pipe-pane -t testsess:win1 -o \"cat >> /tmp/tmux_pipe.log\" 2>&1 || true" 0 "pipe-pane -o: pipe output"
    rlRun "tmux respawn-pane -k -t testsess:win1.0 2>&1 " 0 "respawn-pane -k: respawn"
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
