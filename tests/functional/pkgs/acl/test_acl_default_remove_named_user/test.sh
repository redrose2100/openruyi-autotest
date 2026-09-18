#!/bin/bash
# Functional test: acl - default ACL - remove named user from default ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "remove named user from default ACL"
        rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x testdir" 0 "set named user entries"
        rlRun "setfacl -x d:u:daemon testdir" 0 "remove daemon user"
        output=$(getfacl testdir 2>&1)
        rlRun "! echo \"\$output\" | grep -q 'default:user:daemon:'" 0 "daemon removed"
        rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "root preserved" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
