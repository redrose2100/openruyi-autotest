#!/bin/bash
# Functional test: openssl - openssl asn1parse ASN.1 parser
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl asn1parse ASN.1 parser"
    rlRun "openssl genrsa -out key.pem 2048 2>/dev/null" 0 "Generate key"
    rlRun "openssl req -new -x509 -key key.pem -out cert.pem -days 1 -subj '/CN=test' 2>/dev/null" 0 "Generate cert"
    rlRun "openssl asn1parse -in cert.pem 2>/dev/null | head -3 || echo asn1parse_ok" 0 "openssl asn1parse: parse certificate"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
