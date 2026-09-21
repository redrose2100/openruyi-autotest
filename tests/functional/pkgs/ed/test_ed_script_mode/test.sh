#!/bin/bash
# Functional test: ed - Run ed in silent/script mode with -s
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y ed 2>/dev/null || rpm -q ed" 0 "Ensure ed is installed"
    rlPhaseEnd

    rlPhaseStartTest "silent script mode with -s"
        # -s suppresses byte counts and '!' prompt
        printf 'a\ntest\n.\nw test.txt\nq\n' | ed -s 2>err.txt
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed runs in script mode"
        rlAssertExists "test.txt"
        # In -s mode, stderr should be empty (no prompts)
        rlRun "test ! -s err.txt" 0 "No diagnostic output in -s mode"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
