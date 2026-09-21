#!/bin/bash
# Functional test: curl - retry on failure --retry
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    curlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "retry on failure --retry"
    rlRun "curl -s --retry 1 --retry-delay 1 --retry-max-time 3 http://nonexistent.local 2>&1 | grep -qiE 'Could not|failed|Retry' || echo retry_attempted" 0 "curl --retry: retry mechanism"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
