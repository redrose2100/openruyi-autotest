#!/bin/bash
# Functional test: make - make .DEFAULT_GOAL
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    makeSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "make .DEFAULT_GOAL"
    rlRun "echo -e '.DEFAULT_GOAL:=hello\nhello:\n\techo hello\nbye:\n\techo bye' > Makefile" 0 "Create default goal Makefile"
    rlRun "make" 0 "make .DEFAULT_GOAL: non-first target"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
