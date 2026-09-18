#!/bin/bash
# Functional test: acl - setfacl -X remove ACL by rule file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "remove ACL by rule file"
        rlRun "echo 'u:root' > remove_rules.txt" 0 "create remove rules"
        rlRun "setfacl -m u:root:rwx testfile" 0 "pre-set ACL"
        rlRun "setfacl -X remove_rules.txt testfile" 0 "remove by file"
        output=$(getfacl testfile 2>&1)
        rlRun "! echo \"\$output\" | grep -q 'user:root:'" 0 "confirm removed" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
