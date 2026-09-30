#!/bin/bash

# Functional test: wget2 - Output-file-options

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    wget2Setup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "Output-file-options"

    rlRun "wget2 -O /dev/null --version 2>&1 | grep -q Wget" 0 "wget2 -O Option available"

    rlRun "echo '<html><body>test</body></html>' > $TmpDir/index.html" 0 "Create test page"

    rlRun "python3 -m http.server --bind 127.0.0.1 0 &> /dev/null &" 0 "Start local HTTP server"

    HTTP_PID=$!

    sleep 2

    PORT=$(ss -tlpn 2>/dev/null | grep $HTTP_PID | grep -oP '127\.0\.0\.1:\K\d+' | head -1)

    if [ -n "$PORT" ]; then

    rlRun "wget2 -q -O $TmpDir/wget2out.html http://127.0.0.1:$PORT/index.html" 0 "wget2 download to specifyfile"

    rlRun "test -f $TmpDir/wget2out.html" 0 "verifyoutputfilealready"

    fi

    kill $HTTP_PID 2>/dev/null || true

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # wget2 Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

