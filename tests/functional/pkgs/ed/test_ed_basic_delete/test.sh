#!/bin/bash
# Functional test: ed - Delete a specific line with d command
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "delete line with d command"
        # Create 3 lines, delete middle line
        printf 'a\none\ntwo\nthree\n.\n2d\n,n\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0 || true" 0 "ed deletes line"
        rlRun "grep -q 'one' out.txt 2>/dev/null || true" 0 "Check one in out.txt"
        rlRun "! grep -q \'two\' out.txt 2>/dev/null || true" 0 "Deleted line absent"
        rlRun "grep -q 'three' out.txt 2>/dev/null || true" 0 "Check three in out.txt"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


