#!/bin/bash
# Functional test: coreutils - comm compare sorted files
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

    rlPhaseStartTest "comm compare sorted files"
    rlRun "sort fruits.txt > sorted1.txt" 0 "Create sorted file 1"
    rlRun "sort fruits.txt > sorted2.txt" 0 "Create sorted file 2"
    rlRun "comm sorted1.txt sorted2.txt" 0 "comm compare files"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
