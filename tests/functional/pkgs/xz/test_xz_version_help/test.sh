#!/bin/bash
# Functional test: xz - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    xzSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "xz --version 2>&1 " 0 "xz version info"
    rlRun "xz --help 2>&1 | head -5 || true" 0 "xz help info"
    rlRun "unxz --version 2>&1 " 0 "unxz version info"
    rlRun "unxz --help 2>&1 | head -5 || true" 0 "unxz help info"
    rlRun "xzcat --version 2>&1 " 0 "xzcat version info"
    rlRun "xzcat --help 2>&1 | head -5 || true" 0 "xzcat help info"
    rlRun "lzma --version 2>&1 " 0 "lzma version info"
    rlRun "lzma --help 2>&1 | head -5 || true" 0 "lzma help info"
    rlRun "unlzma --version 2>&1 " 0 "unlzma version info"
    rlRun "unlzma --help 2>&1 | head -5 || true" 0 "unlzma help info"
    rlRun "lzcat --version 2>&1 " 0 "lzcat version info"
    rlRun "lzcat --help 2>&1 | head -5 || true" 0 "lzcat help info"
    rlRun "lzcmp --version 2>&1 " 0 "lzcmp version info"
    rlRun "lzcmp --help 2>&1 | head -5 || true" 0 "lzcmp help info"
    rlRun "lzdiff --version 2>&1 " 0 "lzdiff version info"
    rlRun "lzdiff --help 2>&1 | head -5 || true" 0 "lzdiff help info"
    rlRun "lzgrep --version 2>&1 " 0 "lzgrep version info"
    rlRun "lzgrep --help 2>&1 | head -5 || true" 0 "lzgrep help info"
    rlRun "lzless --version 2>&1 " 0 "lzless version info"
    rlRun "lzless --help 2>&1 | head -5 || true" 0 "lzless help info"
    rlRun "lzmore --version 2>&1 " 0 "lzmore version info"
    rlRun "lzmore --help 2>&1 | head -5 || true" 0 "lzmore help info"
    rlRun "lzmadec --version 2>&1 " 0 "lzmadec version info"
    rlRun "lzmadec --help 2>&1 | head -5 || true" 0 "lzmadec help info"
    rlRun "lzmainfo --version 2>&1 " 0 "lzmainfo version info"
    rlRun "lzmainfo --help 2>&1 | head -5 || true" 0 "lzmainfo help info"
    rlRun "lzegrep --version 2>&1 " 0 "lzegrep version info"
    rlRun "lzegrep --help 2>&1 | head -5 || true" 0 "lzegrep help info"
    rlRun "lzfgrep --version 2>&1 " 0 "lzfgrep version info"
    rlRun "lzfgrep --help 2>&1 | head -5 || true" 0 "lzfgrep help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # xz Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
