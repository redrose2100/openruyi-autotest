#!/bin/bash
# Functional test: acl - setfacl --restore directory ACL from backup
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "restore directory ACL from backup"
        rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x testdir" 0 "set default ACL"
        rlRun "getfacl testdir > dir.backup" 0 "create dir backup"
        rlRun "setfacl -k testdir" 0 "clear default ACL"
        rlRun "cd $TmpDir && setfacl --restore=dir.backup" 0 "restore dir from backup"
        output=$(getfacl testdir 2>&1)
        rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "default user restored"
        rlRun "echo \"\$output\" | grep -q 'default:group:root:r-x'" 0 "default group restored" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
