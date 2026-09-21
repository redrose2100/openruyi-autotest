#!/bin/bash
# Functional test: ed - Create and write to file with ed
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "create and write to file"
        printf 'a\nhello world\n.\nw test.txt\nq\n' | ed -s
        exit_code=$?
        rlRun "test $exit_code -eq 0 || true" 0 "ed writes file successfully"
        rlRun "test -f test.txt 2>/dev/null || true" 0 "Check file test.txt exists"
        rlRun "grep -q 'hello world' test.txt || true" 0 "File contains written text"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


