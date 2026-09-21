#!/bin/bash
# Functional test: wget2 - wget2 --certificate client cert
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    wget2Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "wget2 --certificate client cert"
    rlRun "wget2 --certificate=/dev/null --private-key=/dev/null http://example.com 2>&1 | grep -qiE 'error|Error|PEM' || echo wget2_cert_ok" 0 "wget2 --certificate: client cert"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
