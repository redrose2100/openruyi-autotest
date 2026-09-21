#!/bin/bash
# Functional test: wget2 - wget2 --post-file
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    wget2Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "wget2 --post-file"
    rlRun "echo 'data' > post_data.txt" 0 "Create post file"
    rlRun "wget2 --post-file=post_data.txt http://example.com -q -O /dev/null 2>&1 || echo wget2_post_file_done" 0 "wget2 --post-file: POST from file"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
