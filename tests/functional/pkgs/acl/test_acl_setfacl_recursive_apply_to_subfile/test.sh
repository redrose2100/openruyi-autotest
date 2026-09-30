#!/bin/bash
# Functional test: acl - setfacl -R apply ACL recursively to sub-files
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir -p testdir" 0 "Create test directory"
        rlRun "touch testdir/file1" 0 "create sub-file" 
    rlPhaseEnd

    rlPhaseStartTest "recursively apply ACL to sub-files"
        rlRun "setfacl -R -m u:root:rwx,g::r--,o::r-- testdir" 0 "recursive setfacl"
        output=$(getfacl testdir/file1 2>&1)
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "sub-file has ACL" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
