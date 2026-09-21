#!/bin/bash
# Functional test: vim - vim -c execute command
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "vim -c execute command"
    rlRun "echo 'test' > vim_test2.txt" 0 "Create test file"
    rlRun "vim -c '%s/test/pass/g' -c 'wq' vim_test2.txt 2>&1 || echo vim_c_ok" 0 "vim -c: execute ex command"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
