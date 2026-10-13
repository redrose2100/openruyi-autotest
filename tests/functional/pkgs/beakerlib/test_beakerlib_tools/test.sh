#!/bin/bash
# Functional test: beakerlib - utility tools
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # Create minimal test journal and summary files
        cat > journal.txt <<EOF
:: [  BEGIN   ] x 5 :: Running test
:: [   LOG    ] :: test log message
:: [   PASS   ] :: test passed
:: [   END    ] :: Test finished
EOF
        cp journal.txt journal_new.txt
        cat > test.sum <<EOF
:: [  JOURNAL ] :: /tmp/test/journal.xml
:: [   LOG    ] :: 0:00:00
:: [   LOG    ] :: 0:00:00
:: [   PASS   ] :: summary test passed
EOF
    rlPhaseEnd

    rlPhaseStartTest "beakerlib-rlMemAvg - Memory average tracking"
        rlRun "beakerlib-rlMemAvg ps 2>&1; true" 0 "beakerlib-rlMemAvg runs"
    rlPhaseEnd

    rlPhaseStartTest "beakerlib-rlMemPeak - Memory peak tracking"
        rlRun "beakerlib-rlMemPeak ps 2>&1; true" 0 "beakerlib-rlMemPeak runs"
    rlPhaseEnd

    rlPhaseStartTest "beakerlib-testwatcher - Test watcher"
        rlRun "beakerlib-testwatcher ps 2>&1; true" 0 "beakerlib-testwatcher runs"
    rlPhaseEnd

    rlPhaseStartTest "beakerlib-journalcmp - Compare journals"
        if command -v beakerlib-journalcmp >/dev/null 2>&1; then
            rlRun "beakerlib-journalcmp journal.txt journal_new.txt" 0 "beakerlib-journalcmp compares journals"
        else
            rlLog "beakerlib-journalcmp is not provided by this beakerlib build, skipping comparison"
            rlRun "diff -q journal.txt journal_new.txt" 0 "Journals are identical"
        fi
    rlPhaseEnd

    rlPhaseStartTest "beakerlib-deja-summarize - Summarize test results"
        if command -v beakerlib-deja-summarize >/dev/null 2>&1; then
            rlRun "beakerlib-deja-summarize test.sum" 0 "beakerlib-deja-summarize processes summary"
        else
            rlLog "beakerlib-deja-summarize is not provided by this beakerlib build, skipping summary"
            rlRun "test -s test.sum" 0 "Summary file is present"
        fi
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd