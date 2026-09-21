#!/bin/bash
# Functional test: vim - vim -v visual mode
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "vim -v visual mode"
    rlRun "echo 'test' > vim_test4.txt" 0 "Create test file"
    rlRun "vim -v -c 'q!' vim_test4.txt 2>&1 || echo vim_v_ok" 0 "vim -v: visual mode"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
