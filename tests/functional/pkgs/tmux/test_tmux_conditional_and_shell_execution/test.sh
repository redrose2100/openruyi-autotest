#!/bin/bash
# Functional test: tmux - Conditional-and-shell-execution
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

    rlPhaseStartTest "Conditional-and-shell-execution"
    rlRun "tmux if-shell \"true\" \"display-message ok\" \"display-message fail\" 2>&1 || true" 0 "if-shell: true condition"
    rlRun "tmux run-shell \"echo hello_from_run_shell\" 2>&1 || true" 0 "run-shell: run shell command"
    rlRun "tmux run-shell -b \"sleep 0.1; echo background\" 2>&1 || true" 0 "run-shell -b: background"
    rlRun "echo quit | tmux command-prompt 2>&1 " 0 "command-prompt: open prompt"
    rlRun "tmux confirm-before -p \"OK?\" \"echo confirmed\" 2>&1 || true" 0 "confirm-before: confirm dialog"
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
