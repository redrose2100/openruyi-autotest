#!/bin/bash
# Functional test: acl - setfacl -M apply ACL from file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "apply ACL from rules file"
        rlRun "echo 'u:root:rw-' > acl_rules.txt" 0 "create rules file"
        rlRun "setfacl -M acl_rules.txt testfile" 0 "apply from file"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
