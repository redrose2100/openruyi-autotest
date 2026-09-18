#!/bin/bash
# Functional test: acl - getfacl backup - save directory default ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "back up directory default ACL entries"
        rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x testdir" 0 "set default ACL"
        rlRun "getfacl testdir 2>&1 | grep 'default:' > out.txt" 0 "get default entries"
        rlAssertGrep "default:user:root:rwx" out.txt
        rlAssertGrep "default:group:root:r-x" out.txt
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
