#!/bin/bash
# Functional test: bash - bash glob wildcards
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    bashSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "bash glob wildcards"
    rlRun "touch glob_test_a.txt glob_test_b.txt glob_test_c.log" 0 "Create glob files"
    rlRun "bash -c 'echo glob_test_*.txt'" 0 "bash glob: *.txt wildcard"
    rlRun "bash -c 'echo glob_test_?.txt'" 0 "bash glob: ? single char"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
