#!/bin/bash
# Functional test: acl - default ACL - new file inherits named entries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "new file inherits named default ACL entries"
        rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x,d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named entries"
        rlRun "touch testdir/newfile" 0 "create new file"
        output=$(getfacl testdir/newfile 2>&1)
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "file inherits user root"
        rlRun "echo \"\$output\" | grep -q 'user:daemon:r-x'" 0 "file inherits user daemon"
        rlRun "echo \"\$output\" | grep -q 'group:root:r-x'" 0 "file inherits group root"
        rlRun "echo \"\$output\" | grep -q 'group:wheel:r--'" 0 "file inherits group wheel" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
