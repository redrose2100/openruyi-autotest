#!/bin/bash
# Functional test: ed - Read and insert content from external file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y ed 2>/dev/null || rpm -q ed" 0 "Ensure ed is installed"
    rlPhaseEnd

    rlPhaseStartTest "read external file with r"
        echo "external content" > ext.txt
        printf 'a\nline1\n.\nr ext.txt\n,n\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed reads external file"
        rlAssertGrep "external content" out.txt "External file content present"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
