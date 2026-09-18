#!/bin/bash
# Functional test: acl - ACL permission - set and verify full ACL entries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "set and verify full ACL entries"
        rlRun "setfacl --set u::rwx,u:root:rwx,g::r-x,o::r--,m::rwx testfile" 0 "set full ACL"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \"\$output\" | grep -q 'user::rwx'" 0 "user::rwx"
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "user:root:rwx"
        rlRun "echo \"\$output\" | grep -q 'group::r-x'" 0 "group::r-x"
        rlRun "echo \"\$output\" | grep -q 'mask::rwx'" 0 "mask::rwx" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
