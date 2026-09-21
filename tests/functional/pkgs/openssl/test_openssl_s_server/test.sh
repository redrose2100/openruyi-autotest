#!/bin/bash
# Functional test: openssl - openssl s_server TLS server
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl s_server TLS server"
    rlRun "openssl genrsa -out server.key 2048 2>/dev/null" 0 "Generate server key"
    rlRun "openssl req -new -x509 -key server.key -out server.crt -days 1 -subj '/CN=localhost' 2>/dev/null" 0 "Generate self-signed cert"
    rlRun "timeout 2 openssl s_server -cert server.crt -key server.key -port 9443 2>/dev/null &" 0 "openssl s_server: start (background)"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
