#!/bin/bash
# Functional test: ed - Insert text before current line with i command
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "insert text before line"
        # Create file with line2, then insert line1 before it
        printf 'a\nline2\n.\ni\nline1\n.\n1,2n\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed inserts before line"
        rlAssertGrep "^1\s+line1" out.txt "line1 is first"
        rlAssertGrep "^2\s+line2" out.txt "line2 is second"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
