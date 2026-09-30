#!/bin/bash

# Functional test: openssl - X509֤

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



    rlPhaseStartTest "X509֤"

    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"

    rlRun "cd $TmpDir" 0 "error handlingdirectory"

    rlRun "openssl genrsa -out ca.key 2048" 0 "OpenSSL operation"

    rlRun "openssl req -new -x509 -key ca.key -out ca.crt -days 1 -subj \"/CN=Test\"" 0 "error handlingǩ֤"

    rlRun "openssl x509 -in ca.crt -text -noout | head -10" 0 "OpenSSL operation"

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

