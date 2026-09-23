#!/bin/bash
# Functional test: tmux - Cleanup---kill-sessions
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

    rlPhaseStartTest "Cleanup---kill-sessions"
    rlRun "tmux kill-session -t renamed_sess 2>&1 " 0 "kill-session: kill renamed_sess"
    rlRun "tmux kill-session -t sess_fmt 2>&1 " 0 "kill-session: kill sess_fmt"
    rlRun "tmux kill-session -t sess_sz 2>&1 " 0 "kill-session: kill sess_sz"
    rlRun "tmux kill-session -t sess_flags 2>&1 " 0 "kill-session: kill sess_flags"
    rlRun "tmux kill-session -t sess_env 2>&1 " 0 "kill-session: kill sess_env"
    rlRun "tmux kill-session -t testsess 2>&1 " 0 "kill-session: kill main test session"
    rlRun "tmux kill-server 2>&1 " 0 "kill-server: terminate server"
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
