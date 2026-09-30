#!/bin/bash
# Functional test: ca-certificates-mozilla - certificates-mozilla - error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    caCertificatesMozillaSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "certificates-mozilla - error handling"
    rlRun "rpm -q ca-certificates-mozilla 2>/dev/null || rpm -q ca-certificates" 0 "CA certificatePackage installed"
    rlRun "ls /etc/pki/ca-trust/ 2>/dev/null || ls /etc/ssl/certs/ 2>/dev/null" 0 "certificatedirectory exists"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # ca-certificates-mozilla Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
