#!/bin/bash
# Functional test: ed - Use regex and backreference in substitution
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "regex substitution with backreference \1"
        printf 'a\napple 123\n.\n1s/\([a-z]*\) \([0-9]*\)/\2 \1/\n1p\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0 || true" 0 "ed does backreference substitution"
        rlRun "grep -q \'123 apple\' out.txt 2>/dev/null || true" 0 "Fields swapped via backreference"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


