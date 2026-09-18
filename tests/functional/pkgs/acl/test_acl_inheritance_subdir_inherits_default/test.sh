#!/bin/bash
# Functional test: acl - ACL inheritance - subdirectory inherits default ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "subdirectory inherits default ACL"
        rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x,d:o::r-- testdir" 0 "set default ACL"
        rlRun "mkdir testdir/newsubdir" 0 "create subdirectory"
        output=$(getfacl testdir/newsubdir 2>&1)
        rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "subdir inherits default user"
        rlRun "echo \"\$output\" | grep -q 'default:group:root:r-x'" 0 "subdir inherits default group" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
