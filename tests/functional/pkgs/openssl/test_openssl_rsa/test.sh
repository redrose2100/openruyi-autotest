#!/bin/bash

# Functional test: openssl - RSA

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



    rlPhaseStartTest "RSA"

    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"

    rlRun "cd $TmpDir" 0 "error handlingdirectory"

    rlRun "openssl genrsa -out key.pem 2048" 0 "OpenSSL operation"

    rlRun "test -f key.pem" 0 "Test operation"

    rlRun "openssl rsa -in key.pem -pubout -out pub.pem" 0 "OpenSSL operation"

    rlRun "test -f pub.pem" 0 "Test operation"

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

