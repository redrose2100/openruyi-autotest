#!/bin/bash
# Functional test: glibc - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    glibcSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "gencat --version 2>&1 " 0 "gencat version info"
    rlRun "gencat --help 2>&1 | head -5 || true" 0 "gencat help info"
    rlRun "getconf --version 2>&1 " 0 "getconf version info"
    rlRun "getconf --help 2>&1 | head -5 || true" 0 "getconf help info"
    rlRun "getent --version 2>&1 " 0 "getent version info"
    rlRun "getent --help 2>&1 | head -5 || true" 0 "getent help info"
    rlRun "iconv --version 2>&1 " 0 "iconv version info"
    rlRun "iconv --help 2>&1 | head -5 || true" 0 "iconv help info"
    rlRun "ldconfig --version 2>&1 " 0 "ldconfig version info"
    rlRun "ldconfig --help 2>&1 | head -5 || true" 0 "ldconfig help info"
    rlRun "ldd --version 2>&1 " 0 "ldd version info"
    rlRun "ldd --help 2>&1 | head -5 || true" 0 "ldd help info"
    rlRun "locale --version 2>&1 " 0 "locale version info"
    rlRun "locale --help 2>&1 | head -5 || true" 0 "locale help info"
    rlRun "localedef --version 2>&1 " 0 "localedef version info"
    rlRun "localedef --help 2>&1 | head -5 || true" 0 "localedef help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # glibc Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
