#!/bin/bash
# Functional test: openssl - openssl pkcs12 PKCS#12 bundle
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl pkcs12 PKCS#12 bundle"
    rlRun "openssl genrsa -out p12key.pem 2048 2>/dev/null" 0 "Generate key"
    rlRun "openssl req -new -x509 -key p12key.pem -out p12cert.pem -days 1 -subj '/CN=test' 2>/dev/null" 0 "Generate cert"
    rlRun "openssl pkcs12 -export -in p12cert.pem -inkey p12key.pem -out test.p12 -passout pass:test123 2>/dev/null" 0 "openssl pkcs12: create bundle"
    rlRun "test -f test.p12" 0 "openssl pkcs12: bundle created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
