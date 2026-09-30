#!/bin/bash

# Functional test: openssl - error handling

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



    rlPhaseStartTest "error handling"

    rlRun "openssl version" 0 "OpenSSL operation"

    rlRun "openssl help 2>&1 | head -20" 0 "OpenSSL operation"

    rlRun "openssl list -standard-commands 2>&1 | head -10" 0 "OpenSSL operation"

    rlRun "openssl list -cipher-commands 2>&1 | head -10" 0 "OpenSSL operation"

    rlRun "openssl list -digest-commands 2>&1 | head -10" 0 "OpenSSL operation"

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

