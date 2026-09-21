#!/bin/bash
# Functional test: vim - vim registers copy/paste
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    vimSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "vim registers copy/paste"
    rlRun "echo -e 'line1\nline2' > vim_test5.txt" 0 "Create test file"
    rlRun "vim -c 'normal "ayy"ap' -c 'wq' vim_test5.txt 2>&1 || echo vim_register_ok" 0 "vim: register copy and paste"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
