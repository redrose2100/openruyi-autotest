#!/bin/bash
# Functional test: acl - ACL permission - mask truncates effective permissions
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "mask truncates effective permissions"
        rlRun "setfacl -m u:root:rwx,m::r-- testfile" 0 "set mask limited"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \"\$output\" | grep -q 'mask::r--'" 0 "mask::r--"
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "entry preserved"
        rlRun "getfacl -e testfile > out.txt 2>&1" 0 "show effective permissions"
        rlAssertGrep "user:root:rwx.*#effective:r--" out.txt
        rlAssertGrep "group::r--.*#effective:r--" out.txt
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
