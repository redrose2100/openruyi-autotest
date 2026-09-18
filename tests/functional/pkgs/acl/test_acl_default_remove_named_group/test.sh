#!/bin/bash
# Functional test: acl - default ACL - remove named group from default ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "remove named group from default ACL"
        rlRun "setfacl -m d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named group entries"
        rlRun "setfacl -x d:g:wheel testdir" 0 "remove wheel group"
        output=$(getfacl testdir 2>&1)
        rlRun "! echo \"\$output\" | grep -q 'default:group:wheel:'" 0 "wheel removed" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
