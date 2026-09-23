#!/bin/bash
# Functional test: tmux - Server-management
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

    rlPhaseStartTest "Server-management"
    rlRun "tmux start-server" 0 "start-server: start tmux server"
    rlRun "tmux list-sessions 2>&1 " 0 "list-sessions: initial state"
    rlRun "tmux has-session -t test 2>&1 " 0 "has-session: check nonexistent"
    rlRun "tmux list-clients 2>&1 " 0 "list-clients: list connected clients"
    rlRun "tmux list-commands | head -20" 0 "list-commands: list all commands"
    rlRun "tmux lscm new-session" 0 "list-commands: filter specific command"
    rlRun "tmux lscm -F \"#{command}\" | head -10" 0 "list-commands: format output"
    rlRun "tmux server-access -l 2>&1 " 0 "server-access -l: list access"
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
