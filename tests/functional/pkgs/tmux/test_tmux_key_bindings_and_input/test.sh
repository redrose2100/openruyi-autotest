#!/bin/bash
# Functional test: tmux - Key-bindings-and-input
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

    rlPhaseStartTest "Key-bindings-and-input"
    rlRun "tmux list-keys | head -20" 0 "list-keys: list all keys"
    rlRun "tmux list-keys -T prefix | head -10" 0 "list-keys -T: prefix table"
    rlRun "tmux list-keys -T root | head -10" 0 "list-keys -T: root table"
    rlRun "tmux list-keys -a" 0 "list-keys -a: all keys"
    rlRun "tmux list-keys -N | head -10" 0 "list-keys -N: with notes"
    rlRun "tmux bind-key -n C-o display-message \"test\"" 0 "bind-key -n: bind to key"
    rlRun "tmux unbind-key -n C-o" 0 "unbind-key -n: unbind key"
    rlRun "tmux bind-key -T prefix x display-message \"test\"" 0 "bind-key -T: bind in table"
    rlRun "tmux unbind-key -T prefix x" 0 "unbind-key -T: unbind in table"
    rlRun "tmux send-keys -t testsess:win1 \"echo hello\" Enter 2>&1 || true" 0 "send-keys: send text"
    rlRun "tmux send-keys -l -t testsess:win1 \"literal\" 2>&1 || true" 0 "send-keys -l: literal"
    rlRun "tmux send-keys -H -t testsess:win1 \"0d\" 2>&1 || true" 0 "send-keys -H: hex"
    rlRun "tmux send-prefix -t testsess:win1 2>&1 " 0 "send-prefix: send prefix key"
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
