#!/bin/bash
# Functional test: libtasn1 - error handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    libtasn1Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "error handling"
    rlRun "asn1Coding --invalid-flag-xyz 2>&1 " 0 " asn1Coding Чerror handling"
    rlRun "asn1Decoding --invalid-flag-xyz 2>&1 " 0 " asn1Decoding Чerror handling"
    rlRun "asn1Parser --invalid-flag-xyz 2>&1 " 0 " asn1Parser Чerror handling"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # libtasn1 Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
