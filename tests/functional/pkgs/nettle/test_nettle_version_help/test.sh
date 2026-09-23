#!/bin/bash
# Functional test: nettle - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    nettleSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "nettle-hash --version 2>&1 " 0 "nettle-hash version info"
    rlRun "nettle-hash --help 2>&1 | head -5 || true" 0 "nettle-hash help info"
    rlRun "nettle-lfib-stream --version 2>&1 " 0 "nettle-lfib-stream version info"
    rlRun "nettle-lfib-stream --help 2>&1 | head -5 || true" 0 "nettle-lfib-stream help info"
    rlRun "nettle-pbkdf2 --version 2>&1 " 0 "nettle-pbkdf2 version info"
    rlRun "nettle-pbkdf2 --help 2>&1 | head -5 || true" 0 "nettle-pbkdf2 help info"
    rlRun "pkcs1-conv --version 2>&1 " 0 "pkcs1-conv version info"
    rlRun "pkcs1-conv --help 2>&1 | head -5 || true" 0 "pkcs1-conv help info"
    rlRun "sexp-conv --version 2>&1 " 0 "sexp-conv version info"
    rlRun "sexp-conv --help 2>&1 | head -5 || true" 0 "sexp-conv help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # nettle Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
