#!/bin/bash
# Functional test: tmux - Buffer-management
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

    rlPhaseStartTest "Buffer-management"
    rlRun "echo \"test buffer content\" | tmux set-buffer -b testbuf" 0 "set-buffer -b: named buffer"
    rlRun "tmux set-buffer -b buf2 \"hello world\"" 0 "set-buffer: direct data"
    rlRun "tmux set-buffer -a -b testbuf \" appended\"" 0 "set-buffer -a: append"
    rlRun "tmux list-buffers" 0 "list-buffers: list all buffers"
    rlRun "tmux list-buffers -F \"#{buffer_name}: #{buffer_sample}\"" 0 "list-buffers -F: formatted"
    rlRun "tmux show-buffer -b testbuf" 0 "show-buffer: show buffer contents"
    rlRun "tmux paste-buffer -b testbuf -t testsess:win1 2>&1 " 0 "paste-buffer: paste buffer"
    rlRun "tmux paste-buffer -d -b testbuf 2>&1 " 0 "paste-buffer -d: delete after paste"
    rlRun "tmux set-buffer -b todelete \"temp\"" 0 "delete-buffer: create temp buffer"
    rlRun "tmux delete-buffer -b todelete" 0 "delete-buffer: delete buffer"
    rlRun "tmux set-buffer -b savebuf \"save test\"" 0 "save-buffer: create buffer"
    rlRun "tmux save-buffer -b savebuf /tmp/tmux_save.txt 2>&1 " 0 "save-buffer: save to file"
    rlRun "tmux load-buffer -b loadbuf /tmp/tmux_save.txt 2>&1 " 0 "load-buffer: load from file"
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
