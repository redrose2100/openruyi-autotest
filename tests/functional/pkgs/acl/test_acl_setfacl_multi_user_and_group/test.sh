#!/bin/bash
# Functional test: acl - setfacl - set multiple user and group ACL entries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "set multiple user and group ACL entries"
        rlRun "setfacl -m u:root:rwx,u:daemon:r-x,g:root:r--,g:wheel:rw- testfile" 0 "set multi ACL"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "user root"
        rlRun "echo \"\$output\" | grep -q 'user:daemon:r-x'" 0 "user daemon"
        rlRun "echo \"\$output\" | grep -q 'group:root:r--'" 0 "group root"
        rlRun "echo \"\$output\" | grep -q 'group:wheel:rw-'" 0 "group wheel" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
