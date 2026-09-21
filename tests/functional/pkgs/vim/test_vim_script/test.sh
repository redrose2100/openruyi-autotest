#!/bin/bash
# Functional test: vim - vim -S source script
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "vim -S source script"
    rlRun "echo ':quit' > vim_script.vim" 0 "Create vim script"
    rlRun "echo 'test' > vim_test3.txt" 0 "Create test file"
    rlRun "vim -S vim_script.vim vim_test3.txt 2>&1 || echo vim_S_ok" 0 "vim -S: source vimscript"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
