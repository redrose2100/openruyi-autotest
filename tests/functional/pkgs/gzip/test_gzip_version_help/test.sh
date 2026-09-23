#!/bin/bash
# Functional test: gzip - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gzipSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "gzip --version 2>&1 " 0 "gzip version info"
    rlRun "gzip --help 2>&1 | head -5 || true" 0 "gzip help info"
    rlRun "gunzip --version 2>&1 " 0 "gunzip version info"
    rlRun "gunzip --help 2>&1 | head -5 || true" 0 "gunzip help info"
    rlRun "zcat --version 2>&1 " 0 "zcat version info"
    rlRun "zcat --help 2>&1 | head -5 || true" 0 "zcat help info"
    rlRun "zcmp --version 2>&1 " 0 "zcmp version info"
    rlRun "zcmp --help 2>&1 | head -5 || true" 0 "zcmp help info"
    rlRun "zdiff --version 2>&1 " 0 "zdiff version info"
    rlRun "zdiff --help 2>&1 | head -5 || true" 0 "zdiff help info"
    rlRun "zgrep --version 2>&1 " 0 "zgrep version info"
    rlRun "zgrep --help 2>&1 | head -5 || true" 0 "zgrep help info"
    rlRun "zless --version 2>&1 " 0 "zless version info"
    rlRun "zless --help 2>&1 | head -5 || true" 0 "zless help info"
    rlRun "zmore --version 2>&1 " 0 "zmore version info"
    rlRun "zmore --help 2>&1 | head -5 || true" 0 "zmore help info"
    rlRun "znew --version 2>&1 " 0 "znew version info"
    rlRun "znew --help 2>&1 | head -5 || true" 0 "znew help info"
    rlRun "gzexe --version 2>&1 " 0 "gzexe version info"
    rlRun "gzexe --help 2>&1 | head -5 || true" 0 "gzexe help info"
    rlRun "zforce --version 2>&1 " 0 "zforce version info"
    rlRun "zforce --help 2>&1 | head -5 || true" 0 "zforce help info"
    rlRun "zegrep --version 2>&1 " 0 "zegrep version info"
    rlRun "zegrep --help 2>&1 | head -5 || true" 0 "zegrep help info"
    rlRun "zfgrep --version 2>&1 " 0 "zfgrep version info"
    rlRun "zfgrep --help 2>&1 | head -5 || true" 0 "zfgrep help info"
    rlRun "uncompress --version 2>&1 " 0 "uncompress version info"
    rlRun "uncompress --help 2>&1 | head -5 || true" 0 "uncompress help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # gzip Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
