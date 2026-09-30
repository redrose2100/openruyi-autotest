#!/bin/bash
# Functional test: acl - setfacl - export ACL and restore
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "export and restore ACL"
        rlRun "touch testfile" 0 "Create test file"
        rlRun "setfacl -m u:root:rwx,g:root:rwx testfile" 0 "set ACL"
        rlRun "getfacl -R testdir > acl_backup.txt" 0 "export ACL"
        rlRun "setfacl -b testfile" 0 "clear ACL"
        rlRun "setfacl --restore acl_backup.txt" 0 "restore ACL" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
