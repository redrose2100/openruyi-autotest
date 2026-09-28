#!/bin/bash
# Functional test: openssl -ϣ
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "ϣ"
    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"
    rlRun "cd $TmpDir" 0 "error handlingdirectory"
    rlRun "echo \"test data\" > testfile" 0 "error handlingļ"
    rlRun "openssl dgst -md5 testfile" 0 "MD5 ժҪ"
    rlRun "openssl dgst -sha256 testfile" 0 "SHA256 ժҪ"
    rlRun "openssl dgst -sha512 testfile" 0 "SHA512 ժҪ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # openssl Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
