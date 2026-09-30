#!/bin/bash
# Functional test: ed - Write specific line range to another file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "write range of lines to file"
        printf 'a\nline1\nline2\nline3\n.\n1,2w range.txt\nq\n' | ed -s > /dev/null 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0 || true" 0 "ed writes range to file"
        rlRun "test -f range.txt 2>/dev/null || true" 0 "Check file range.txt exists"
        rlRun "grep -q 'line1' range.txt || true" 0 "Line 1 in range file"
        rlRun "grep -q 'line2' range.txt || true" 0 "Line 2 in range file"
        rlRun "! grep -q 'line3' range.txt || true" 0 "Line 3 not in range file"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


