#!/bin/bash
# Functional test: tmux - Window-management
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

    rlPhaseStartTest "Window-management"
    rlRun "tmux new-window -t testsess -n win2" 0 "new-window: create window"
    rlRun "tmux new-window -t testsess -n win3 -d" 0 "new-window -d: detached"
    rlRun "tmux new-window -t testsess -c /tmp -n tmpwin" 0 "new-window -c: with directory"
    rlRun "tmux new-window -t testsess -n envwin -e MYVAR=test" 0 "new-window -e: with env"
    rlRun "tmux list-windows -t testsess" 0 "list-windows: list all windows"
    rlRun "tmux list-windows -a" 0 "list-windows -a: all sessions"
    rlRun "tmux list-windows -t testsess -F \"#{window_name}\"" 0 "list-windows -F: formatted"
    rlRun "tmux select-window -t testsess:win1" 0 "select-window: by name"
    rlRun "tmux select-window -t testsess:1" 0 "select-window: by index"
    rlRun "tmux select-window -l" 0 "select-window -l: last window"
    rlRun "tmux select-window -n" 0 "select-window -n: next"
    rlRun "tmux select-window -p" 0 "select-window -p: previous"
    rlRun "tmux rename-window -t testsess:tmpwin tmp_renamed" 0 "rename-window: rename window"
    rlRun "tmux next-window -t testsess" 0 "next-window: next"
    rlRun "tmux previous-window -t testsess" 0 "previous-window: prev"
    rlRun "tmux last-window -t testsess" 0 "last-window: last"
    rlRun "tmux move-window -t testsess:envwin -a" 0 "move-window -a: after"
    rlRun "tmux move-window -t testsess:envwin -b" 0 "move-window -b: before"
    rlRun "tmux swap-window -s testsess:win1 -t testsess:win2" 0 "swap-window"
    rlRun "tmux link-window -s testsess:win1 -t renamed_sess:linked" 0 "link-window: link window"
    rlRun "tmux unlink-window -t renamed_sess:linked" 0 "unlink-window: unlink"
    rlRun "tmux new-window -t testsess -n tokill" 0 "kill-window: create temp window"
    rlRun "tmux kill-window -t testsess:tokill" 0 "kill-window: kill window"
    rlRun "tmux rotate-window -t testsess" 0 "rotate-window: rotate"
    rlRun "tmux rotate-window -D -t testsess" 0 "rotate-window -D: downward"
    rlRun "tmux respawn-window -k -t testsess:win3 2>&1 " 0 "respawn-window -k: respawn"
    rlRun "tmux resize-window -t testsess:win1 -x 100 -y 30 2>&1 " 0 "resize-window: set size"
    rlRun "tmux resize-window -t testsess:win1 -U 2>&1 " 0 "resize-window -U: up"
    rlRun "tmux resize-window -t testsess:win1 -D 2>&1 " 0 "resize-window -D: down"
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
