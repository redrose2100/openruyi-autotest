#!/bin/bash
# Functional test: acl - ACL permission - raise mask restores effective permissions
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "raise mask to restore effective permissions"
        rlRun "setfacl -m u:root:rwx testfile" 0 "set user ACL"
        rlRun "setfacl -m m::rwx testfile" 0 "raise mask to rwx"
        rlRun "getfacl -e testfile > out.txt 2>&1" 0 "show effective permissions"
        rlAssertGrep "user:root:rwx.*#effective:rwx" out.txt
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
