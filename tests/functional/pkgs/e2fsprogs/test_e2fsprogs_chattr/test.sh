#!/bin/bash
# Functional test: e2fsprogs - chattr/lsattr file attributes
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        e2fsprogsSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "test content" > testfile.txt
        echo "another file" > another.txt
    rlPhaseEnd

    rlPhaseStartTest "chattr +i immutable attribute"
        rlRun "chattr +i testfile.txt" 0 "Set immutable (+i) attribute"
        rlRun "lsattr testfile.txt | grep -q -- '----i'" 0 "lsattr confirms +i is set"
        echo "new line" >> testfile.txt 2>/dev/null
        rlRun "test $? -ne 0" 0 "Write fails on immutable file"
        rlRun "chattr -i testfile.txt" 0 "Remove immutable attribute"
    rlPhaseEnd

    rlPhaseStartTest "chattr +a append-only attribute"
        rlRun "chattr +a testfile.txt" 0 "Set append-only (+a) attribute"
        rlRun "lsattr testfile.txt | grep -q -- '-----a'" 0 "lsattr confirms +a is set"
        rlRun "chattr -a testfile.txt" 0 "Remove append-only attribute"
    rlPhaseEnd

    rlPhaseStartTest "lsattr listing"
        rlRun "lsattr testfile.txt another.txt | wc -l | grep -E '[23]'" 0 "lsattr lists attributes for multiple files"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd