#!/bin/bash
# Functional test: acl - setfacl -R -b recursively remove ACL
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir -p testdir/subdir1" 0 "create nested dirs"
        rlRun "touch testdir/file1 testdir/subdir1/file2" 0 "create test files"
        rlRun "setfacl -R -m u:root:rw- testdir" 0 "pre-set ACL" 
    rlPhaseEnd

    rlPhaseStartTest "recursively remove ACL from all files"
        rlRun "setfacl -R -b testdir" 0 "recursive remove ACL"
        output1=$(getfacl testdir/file1 2>&1)
        output2=$(getfacl testdir/subdir1/file2 2>&1)
        rlRun "! echo \"\$output1\" | grep -q 'user:root:'" 0 "verify file1 cleared"
        rlRun "! echo \"\$output2\" | grep -q 'user:root:'" 0 "verify subdir1/file2 cleared" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
