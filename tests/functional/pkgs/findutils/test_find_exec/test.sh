#!/bin/bash
# Functional test: findutils - find -exec execute command
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    findutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "mkdir -p find_testdir" 0 "Create test directory"

    rlPhaseEnd

    rlPhaseStartTest "find -exec execute command"
    rlRun "touch find_testdir/e1.txt find_testdir/e2.txt" 0 "Create exec test files"
    rlRun "find find_testdir -name 'e*.txt' -exec wc -l {} \;" 0 "find -exec: run wc on each file"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
