#!/bin/bash
# Functional test: openssl - openssl pkey key operations
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    opensslSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "openssl pkey key operations"
    rlRun "openssl genrsa -out test.key 2048 2>/dev/null" 0 "Generate RSA key"
    rlRun "openssl pkey -in test.key -pubout -out test.pub 2>/dev/null" 0 "openssl pkey: extract public key"
    rlRun "test -f test.pub" 0 "openssl pkey: public key created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
