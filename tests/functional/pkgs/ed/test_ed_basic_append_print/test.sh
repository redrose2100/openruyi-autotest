#!/bin/bash
# Functional test: ed - Append text to buffer and print it
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "append text and print line"
        printf 'a\nline1\nline2\n.\n1p\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed prints lines"
        rlAssertGrep "line1" out.txt
        rlAssertNotGrep "line2" out.txt "Only prints addressed line"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
