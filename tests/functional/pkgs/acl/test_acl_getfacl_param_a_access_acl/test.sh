#!/bin/bash
# Functional test: acl - getfacl -a show access ACL only
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "use -a to show access ACL only"
        rlRun "getfacl -a testfile > out.txt 2>&1" 0 "getfacl -a"
        rlAssertGrep "user::" out.txt
        if getfacl -a testfile 2>&1 | grep -q "default:"; then
            rlFail "-a output contains default entries"
        else
            rlPass "-a output contains no default entries"
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
