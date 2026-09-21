#!/bin/bash
# Functional test: bash - bash arithmetic $(( ))
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    bashSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "bash arithmetic $(( ))"
    rlRun "bash -c 'echo \$(( 2 + 3 ))'" 0 "bash: \$(( )) arithmetic"
    rlRun "bash -c 'echo \$(( 10 * 5 ))'" 0 "bash: \$(( )) multiplication"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
