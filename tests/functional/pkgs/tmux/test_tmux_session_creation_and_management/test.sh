#!/bin/bash
# Functional test: tmux - Session-creation-and-management
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

    rlPhaseStartTest "Session-creation-and-management"
    rlRun "tmux new-session -d -s testsess -n win1" 0 "new-session -d: create detached session"
    rlRun "tmux has-session -t testsess" 0 "has-session: verify session exists"
    rlRun "tmux new-session -d -s sess2 -c /tmp -n main" 0 "new-session -d: with start directory"
    rlRun "tmux has-session -t sess2" 0 "has-session: verify sess2 exists"
    rlRun "tmux new-session -d -s sess_env -e TEST_VAR=hello -n env_win" 0 "new-session -e: set environment"
    rlRun "tmux new-session -d -s sess_fmt -F \"#{session_name}\" -n fmt_win" 0 "new-session -F: format output"
    rlRun "tmux new-session -d -s sess_sz -x 80 -y 24 -n sz_win" 0 "new-session: set dimensions"
    rlRun "tmux new-session -d -s sess_flags -A -n flags_win 2>&1 " 0 "new-session -A: attach if exists"
    rlRun "tmux list-sessions" 0 "list-sessions: list all sessions"
    rlRun "tmux list-sessions -F \"#{session_name}\"" 0 "list-sessions -F: formatted"
    rlRun "tmux rename-session -t sess2 renamed_sess" 0 "rename-session: rename sess2"
    rlRun "tmux has-session -t renamed_sess" 0 "has-session: verify renamed session"
    rlRun "tmux lock-session -t testsess 2>&1 " 0 "lock-session: lock session"
    rlRun "tmux switch-client -t renamed_sess 2>&1 " 0 "switch-client -t: switch to session"
    rlRun "tmux attach-session -t testsess -d 2>&1 " 0 "attach-session -d: attach and detach others"
    rlRun "tmux detach-client -P 2>&1 " 0 "detach-client -P"
    rlRun "tmux detach-client -a -s testsess 2>&1 " 0 "detach-client -a: all in session"
    rlRun "tmux suspend-client -t testsess 2>&1 " 0 "suspend-client: suspend client"
    rlRun "tmux lock-client -t testsess 2>&1 " 0 "lock-client: lock client"
    rlRun "tmux refresh-client -S 2>&1 " 0 "refresh-client -S: status line only"
    rlRun "tmux refresh-client -L 2>&1 " 0 "refresh-client -L: lease"
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
