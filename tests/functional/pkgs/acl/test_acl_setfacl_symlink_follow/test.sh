#!/bin/bash
# Functional test: acl - setfacl -L follow symlink to set ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
        rlRun "ln -s testfile symlink" 0 "create symlink" 
    rlPhaseEnd

    rlPhaseStartTest "use -L to follow symlink"
        rlRun "setfacl -L -m u:root:rwx symlink" 0 "setfacl -L"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "symlink target has ACL" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
