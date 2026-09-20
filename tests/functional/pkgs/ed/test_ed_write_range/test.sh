#!/bin/bash
# Functional test: ed - Write specific line range to another file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "write range of lines to file"
        printf 'a\nline1\nline2\nline3\n.\n1,2w range.txt\nq\n' | ed -s > /dev/null 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed writes range to file"
        rlAssertExists "range.txt"
        rlRun "grep -q 'line1' range.txt" 0 "Line 1 in range file"
        rlRun "grep -q 'line2' range.txt" 0 "Line 2 in range file"
        rlRun "! grep -q 'line3' range.txt" 0 "Line 3 not in range file"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
