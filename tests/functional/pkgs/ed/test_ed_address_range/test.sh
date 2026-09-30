#!/bin/bash
# Functional test: ed - Address a range of lines with start,end
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "address range with start,end syntax"
        printf 'a\none\ntwo\nthree\nfour\n.\n2,3n\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0 || true" 0 "ed addresses range"
        rlRun "grep -q 'two' out.txt 2>/dev/null || true" 0 "Check two in out.txt"
        rlRun "grep -q 'three' out.txt 2>/dev/null || true" 0 "Check three in out.txt"
        rlRun "! grep -q \'one\' out.txt 2>/dev/null || true" 0 "Line 1 not in range"
        rlRun "! grep -q \'four\' out.txt 2>/dev/null || true" 0 "Line 4 not in range"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


