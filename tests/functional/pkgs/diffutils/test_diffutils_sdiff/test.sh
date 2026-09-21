#!/bin/bash
# Functional test: diffutils - sdiff basic usage
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    diffutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "sdiff basic usage"
    rlRun "echo 'line1
line2' > a.txt && echo 'line1
line3' > b.txt" 0 "Create test files"
    rlRun "sdiff a.txt b.txt 2>&1 | head -5" 0 "sdiff: side-by-side diff"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
