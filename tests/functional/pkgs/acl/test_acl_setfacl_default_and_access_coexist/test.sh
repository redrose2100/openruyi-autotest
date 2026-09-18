#!/bin/bash
# Functional test: acl - setfacl - default and access ACL coexist on directory
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "default and access ACL coexist on directory"
        rlRun "setfacl -m d:u:root:rwx,d:g::r-x,d:o::r-x testdir" 0 "set default ACL"
        rlRun "setfacl -m u:root:rwx,g::r-x,o::r-x testdir" 0 "set access ACL"
        output=$(getfacl testdir 2>&1)
        rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "default ACL present"
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "access ACL present" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
