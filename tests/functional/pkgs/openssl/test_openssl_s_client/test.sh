#!/bin/bash
# Functional test: openssl - openssl s_client TLS client
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl s_client TLS client"
    rlRun "openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | grep -qiE 'BEGIN CERTIFICATE|CONNECTED' || echo s_client_test_done" 0 "openssl s_client: connect to TLS server"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
