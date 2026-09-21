#!/bin/bash
# Functional test: bash - bash variable expansion
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    bashSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "bash variable expansion"
    rlRun "bash -c 'name=world; echo \${name}'" 0 "bash: \${var} expansion"
    rlRun "bash -c 'name=hello.txt; echo \${name%.txt}'" 0 "bash: \${var%} suffix removal"
    rlRun "bash -c 'name=hello.txt; echo \${name#*.}'" 0 "bash: \${var#} prefix removal"
    rlRun "bash -c 'text=abc; echo \${#text}'" 0 "bash: \${#} string length"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
