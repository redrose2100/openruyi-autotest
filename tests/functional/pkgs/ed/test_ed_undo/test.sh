#!/bin/bash
# Functional test: ed - Undo the last modification with u
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "echo '${TEST_SERVER_1_PASSWORD:-openruyi}' | sudo -S dnf install -y ed 2>/dev/null || rpm -q ed" 0 "Ensure ed is installed"
    rlPhaseEnd

    rlPhaseStartTest "undo last change with u"
        printf 'a\nhello\n.\n1s/hello/world/\nu\n1p\nq\n' | ed -s > out.txt 2>&1
        exit_code=$?
        rlRun "test $exit_code -eq 0" 0 "ed undoes change"
        rlAssertGrep "hello" out.txt "Undo restored original text"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
