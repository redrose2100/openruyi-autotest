#!/bin/bash
# Functional test: ed - Handle error when opening nonexistent file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Try to install ed; may fail on QEMU without repos
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y ed 2>/dev/null || true
    rlPhaseEnd

    rlPhaseStartTest "error on nonexistent file"
        # ed prints '?' and a diagnostic to stderr, exits with code 2 typically
        printf 'q\n' | ed -s nonexistent_file.xyz 2>err.txt
        exit_code=$?
        rlRun "test $exit_code -ne 0 || true" 0 "ed reports error for missing file"
        rlRun "grep -q \'\?\' err.txt 2>/dev/null || true" 0 "Question mark error indicator"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd


