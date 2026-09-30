#!/bin/bash
# Functional test: coreutils - uniq filter repeated lines
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo 'hello world' > file1.txt" 0 "Create test file"
    rlRun "echo 'line 1' > lines.txt" 0 "Create lines file"
    for i in $(seq 2 20); do echo "line $i" >> lines.txt; done
    rlRun "mkdir a" 0 "Create directory a"
    rlRun "mkdir ls_testdir" 0 "Create test directory"
    rlRun "echo 'a,b,c' > csv.txt" 0 "Create CSV file"
    rlRun "echo -e 'apple\norange\nbanana\napple' > fruits.txt" 0 "Create fruits file"

    rlPhaseEnd

    rlPhaseStartTest "uniq filter repeated lines"
    rlRun "sort fruits.txt | uniq" 0 "uniq unique lines"
    rlRun "test $(sort fruits.txt | uniq | wc -l) -eq 3" 0 "uniq: 3 unique"
    rlRun "sort fruits.txt | uniq -c" 0 "uniq -c count occurrences"
    rlRun "sort fruits.txt | uniq -d" 0 "uniq -d only duplicates"
    rlRun "sort fruits.txt | uniq -u" 0 "uniq -u only uniques"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
