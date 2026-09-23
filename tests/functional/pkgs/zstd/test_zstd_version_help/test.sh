#!/bin/bash
# Functional test: zstd - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    zstdSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "zstd --version 2>&1 " 0 "zstd version info"
    rlRun "zstd --help 2>&1 | head -5 || true" 0 "zstd help info"
    rlRun "unzstd --version 2>&1 " 0 "unzstd version info"
    rlRun "unzstd --help 2>&1 | head -5 || true" 0 "unzstd help info"
    rlRun "zstdcat --version 2>&1 " 0 "zstdcat version info"
    rlRun "zstdcat --help 2>&1 | head -5 || true" 0 "zstdcat help info"
    rlRun "zstdgrep --version 2>&1 " 0 "zstdgrep version info"
    rlRun "zstdgrep --help 2>&1 | head -5 || true" 0 "zstdgrep help info"
    rlRun "zstdless --version 2>&1 " 0 "zstdless version info"
    rlRun "zstdless --help 2>&1 | head -5 || true" 0 "zstdless help info"
    rlRun "zstdmt --version 2>&1 " 0 "zstdmt version info"
    rlRun "zstdmt --help 2>&1 | head -5 || true" 0 "zstdmt help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # zstd Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
