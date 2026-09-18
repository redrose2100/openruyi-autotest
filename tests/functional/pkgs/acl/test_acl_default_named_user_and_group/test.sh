#!/bin/bash
# Functional test: acl - default ACL - set named user and group entries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "set named user and group default ACL entries"
        rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x,d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named entries"
        output=$(getfacl testdir 2>&1)
        rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "default user root"
        rlRun "echo \"\$output\" | grep -q 'default:user:daemon:r-x'" 0 "default user daemon"
        rlRun "echo \"\$output\" | grep -q 'default:group:root:r-x'" 0 "default group root"
        rlRun "echo \"\$output\" | grep -q 'default:group:wheel:r--'" 0 "default group wheel" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
