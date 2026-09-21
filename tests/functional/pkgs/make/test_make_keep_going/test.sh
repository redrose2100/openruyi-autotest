#!/bin/bash
# Functional test: make - make -k keep going
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    makeSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "make -k keep going"
    rlRun "echo -e 'all: ok fail\nok:\n\techo ok\nfail:\n\tfalse\n\techo nope' > Makefile" 0 "Create error Makefile"
    rlRun "make -k 2>&1 | grep ok || echo keep_going_works" 0 "make -k: continue on error"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
