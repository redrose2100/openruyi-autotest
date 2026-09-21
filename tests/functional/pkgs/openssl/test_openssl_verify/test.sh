#!/bin/bash
# Functional test: openssl - openssl verify certificate
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl verify certificate"
    rlRun "openssl genrsa -out ca.key 2048 2>/dev/null" 0 "Generate CA key"
    rlRun "openssl req -new -x509 -key ca.key -out ca.crt -days 1 -subj '/CN=TestCA' 2>/dev/null" 0 "Generate CA cert"
    rlRun "openssl genrsa -out server.key 2048 2>/dev/null" 0 "Generate server key"
    rlRun "openssl req -new -key server.key -out server.csr -subj '/CN=server' 2>/dev/null" 0 "Generate CSR"
    rlRun "openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 1 2>/dev/null" 0 "Sign server cert"
    rlRun "openssl verify -CAfile ca.crt server.crt" 0 "openssl verify: verify cert chain"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
