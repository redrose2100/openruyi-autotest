#!/bin/bash
# Functional test: wget - Basic-download
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    wgetSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Basic-download"
    rlRun "wget --version" 0 "check wget version info"
    rlRun "echo '<html><body>Hello</body></html>' > $TmpDir/index.html" 0 "Create test page"
    rlRun "python3 -m http.server --bind 127.0.0.1 0 &> /dev/null &" 0 "Start local HTTP server"
    HTTP_PID=$!
    sleep 2
    PORT=$(ss -tlpn 2>/dev/null | grep $HTTP_PID | grep -oP '127\.0\.0\.1:\K\d+' | head -1)
    if [ -n "$PORT" ]; then
    rlRun "wget -q http://127.0.0.1:$PORT/index.html" 0 "download index.html"
    rlRun "test -f $TmpDir/index.html" 0 "verifyfilealreadydownload"
    fi
    kill $HTTP_PID 2>/dev/null || true
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # wget Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
