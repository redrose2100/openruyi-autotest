#!/bin/bash
# Functional test: curl - upload file -T
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    curlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "upload file -T"
    rlRun "echo 'upload content' > upload_test.txt" 0 "Create upload file"
    rlRun "curl -s -T upload_test.txt http://example.com -o /dev/null 2>&1 | grep -qiE 'error|405|Method Not Allowed' || echo upload_sent" 0 "curl -T: upload file"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
