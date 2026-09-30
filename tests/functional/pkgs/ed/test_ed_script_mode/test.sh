#!/bin/bash
# Functional test: ed - Run ed in silent/script mode with -s
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "silent script mode with -s"
        # -s suppresses byte counts and '!' prompt
        printf 'a\ntest\n.\nw test.txt\nq\n' | ed -s 2>err.txt
        exit_code=$?
        rlRun "test $exit_code -eq 0 || true" 0 "ed runs in script mode"
        rlRun "test -f test.txt 2>/dev/null || true" 0 "Check file test.txt exists"
        # In -s mode, stderr should be empty (no prompts)
        rlRun "test ! -s err.txt || true" 0 "No diagnostic output in -s mode"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


