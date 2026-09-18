#!/bin/bash
# Functional test: acl - getfacl - view default ACL entries on directory
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "view default ACL entries on directory"
        rlRun "setfacl -m d:u::rwx,d:g::r-x,d:o::--- testdir" 0 "set default ACL"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "getfacl testdir"
        rlAssertGrep "default:user::rwx" out.txt
        rlAssertGrep "default:group::r-x" out.txt
        rlAssertGrep "default:other::---" out.txt
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
