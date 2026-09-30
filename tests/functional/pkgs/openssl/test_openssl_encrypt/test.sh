#!/bin/bash

# Functional test: openssl -ӽ

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



    rlPhaseStartTest "ӽ"

    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"

    rlRun "cd $TmpDir" 0 "error handlingdirectory"

    rlRun "echo \"secret message\" > plain.txt" 0 "error handlingļ"

    rlRun "openssl enc -aes-256-cbc -pbkdf2 -in plain.txt -out encrypted.bin -pass pass:test123" 0 "OpenSSL operation"

    rlRun "test -f encrypted.bin" 0 "Test operation"

    rlRun "openssl enc -aes-256-cbc -d -pbkdf2 -in encrypted.bin -out decrypted.txt -pass pass:test123" 0 "OpenSSL operation"

    rlRun "diff plain.txt decrypted.txt" 0 "Compare files line by line"

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

