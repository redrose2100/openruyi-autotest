#!/bin/bash
# Functional test: openssl - openssl req certificate request
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl req certificate request"
    rlRun "openssl genrsa -out req_key.pem 2048 2>/dev/null" 0 "Generate key"
    rlRun "openssl req -new -key req_key.pem -out req.csr -subj '/CN=Test/O=Org/C=US' 2>/dev/null" 0 "openssl req: create CSR"
    rlRun "test -f req.csr" 0 "openssl req: CSR created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
