#!/bin/bash
# Functional test: curl - cookie handling -b/-c
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    curlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "cookie handling -b/-c"
    rlRun "curl -s -c cookie.txt http://example.com" 0 "curl -c: save cookies"
    rlRun "curl -s -b cookie.txt http://example.com" 0 "curl -b: send cookies"
    rlRun "test -f cookie.txt" 0 "curl -c: cookie file created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
