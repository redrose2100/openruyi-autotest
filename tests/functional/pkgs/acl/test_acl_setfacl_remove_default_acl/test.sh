#!/bin/bash
# Functional test: acl - setfacl -k remove default ACL from directory
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "remove default ACL from directory"
        rlRun "setfacl -m d:u:root:rwx testdir" 0 "pre-set default ACL"
        rlRun "setfacl -k testdir" 0 "remove default ACL"
        output=$(getfacl testdir 2>&1)
        rlRun "! echo \"\$output\" | grep -q 'default:'" 0 "confirm no default ACL" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
