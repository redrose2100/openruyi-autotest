#!/bin/bash
# Functional test: ed - Address a range of lines with start,end
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "address range with start,end syntax"
        printf 'a\none\ntwo\nthree\nfour\n.\n2,3n\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed addresses range"
        rlAssertGrep "two" out.txt
        rlAssertGrep "three" out.txt
        rlAssertNotGrep "one" out.txt "Line 1 not in range"
        rlAssertNotGrep "four" out.txt "Line 4 not in range"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
