#!/bin/bash
# Functional test: tmux - Layout-management
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

    rlPhaseStartTest "Layout-management"
    rlRun "tmux select-layout -t testsess:win1 even-horizontal 2>&1 " 0 "select-layout: even-horizontal"
    rlRun "tmux select-layout -t testsess:win1 even-vertical 2>&1 " 0 "select-layout: even-vertical"
    rlRun "tmux select-layout -t testsess:win1 main-horizontal 2>&1 " 0 "select-layout: main-horizontal"
    rlRun "tmux select-layout -t testsess:win1 main-vertical 2>&1 " 0 "select-layout: main-vertical"
    rlRun "tmux select-layout -t testsess:win1 tiled 2>&1 " 0 "select-layout: tiled"
    rlRun "tmux next-layout -t testsess:win1 2>&1 " 0 "next-layout: cycle layouts"
    rlRun "tmux previous-layout -t testsess:win1 2>&1 " 0 "previous-layout: prev layout"
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
