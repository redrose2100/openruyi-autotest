#!/bin/bash
# Functional test: acl - setfacl --restore file ACL from backup
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "restore file ACL from backup"
        rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "set ACL"
        rlRun "getfacl testfile > acl.backup" 0 "create backup"
        rlRun "setfacl -b testfile" 0 "clear ACL"
        rlRun "setfacl --restore=acl.backup" 0 "restore from backup"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "user entry restored"
        rlRun "echo \"\$output\" | grep -q 'group:root:r-x'" 0 "group entry restored" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
