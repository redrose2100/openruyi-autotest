#!/bin/bash
# Functional test: acl - setfacl -m set other readonly
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "set other readonly permission"
        rlRun "setfacl -m o::r-- testfile" 0 "set other readonly"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify ACL"
        rlAssertGrep "other::r--" out.txt
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
