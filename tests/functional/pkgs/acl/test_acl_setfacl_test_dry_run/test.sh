#!/bin/bash
# Functional test: acl - setfacl --test dry run does not modify ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "--test dry run does not modify ACL"
        rlRun "getfacl testfile > before.txt 2>&1" 0 "capture before"
        rlRun "setfacl --test -m u:root:rwx,g:root:--- testfile" 0 "setfacl --test"
        rlRun "getfacl testfile > after.txt 2>&1" 0 "capture after"
        rlRun "diff -u before.txt after.txt" 0 "--test does not modify ACL" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
