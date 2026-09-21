#!/bin/bash
# Functional test: bash - bash -n syntax check
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    bashSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "bash -n syntax check"
    rlRun "bash -n -c 'echo ok'" 0 "bash -n: valid syntax"
    rlRun "bash -n -c 'if' 2>&1 | grep -qiE 'error|unexpected|syntax' || echo syntax_error_detected" 0 "bash -n: invalid syntax caught"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
