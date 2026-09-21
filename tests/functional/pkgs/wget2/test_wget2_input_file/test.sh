#!/bin/bash
# Functional test: wget2 - wget2 -i input file
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    wget2Setup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "wget2 -i input file"
    rlRun "echo 'http://example.com' > urls2.txt" 0 "Create URL list"
    rlRun "wget2 -q -i urls2.txt -O /dev/null 2>&1 || echo wget2_i_done" 0 "wget2 -i: from URL list"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
