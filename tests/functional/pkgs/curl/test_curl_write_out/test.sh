#!/bin/bash
# Functional test: curl - write-out variables -w
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    curlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "write-out variables -w"
    rlRun "curl -s -o /dev/null -w '%{http_code}
' http://example.com" 0 "curl -w: http_code"
    rlRun "curl -s -o /dev/null -w '%{time_total}
' http://example.com" 0 "curl -w: time_total"
    rlRun "curl -s -o /dev/null -w '%{size_download}
' http://example.com" 0 "curl -w: size_download"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
