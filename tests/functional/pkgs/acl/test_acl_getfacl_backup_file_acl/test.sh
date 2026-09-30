#!/bin/bash
# Functional test: acl - getfacl backup - save file ACL to backup
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "back up file ACL"
        rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "set ACL"
        rlRun "getfacl testfile > acl.backup" 0 "getfacl backup"
        rlRun "test -f acl.backup" 0 "backup file created"
        rlRun "grep -q '^# file:' acl.backup" 0 "backup has file header" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
