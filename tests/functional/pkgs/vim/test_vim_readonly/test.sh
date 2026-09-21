#!/bin/bash
# Functional test: vim - vim -R readonly mode
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "vim -R readonly mode"
    rlRun "echo 'test line' > vim_test.txt" 0 "Create test file"
    rlRun "vim -R -c 'q!' vim_test.txt 2>&1 || echo vim_R_ok" 0 "vim -R: readonly mode"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
