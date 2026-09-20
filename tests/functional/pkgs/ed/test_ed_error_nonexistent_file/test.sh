#!/bin/bash
# Functional test: ed - Handle error when opening nonexistent file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "error on nonexistent file"
        # ed prints '?' and a diagnostic to stderr, exits with code 2 typically
        printf 'q\n' | ed -s nonexistent_file.xyz 2>err.txt
        exit_code=$?
        rlRun "test $exit_code -ne 0" 0 "ed reports error for missing file"
        rlAssertGrep "\?" err.txt "Question mark error indicator"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
