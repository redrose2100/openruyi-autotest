#!/bin/bash

# Functional test: acl - setfacl recursive

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    aclSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlRun "mkdir -p testdir/subdir1/subdir2" 0 "createmultisubdirectory"

    rlRun "touch testdir/file1 testdir/subdir1/file2" 0 "Create test file"

    rlPhaseEnd



    rlPhaseStartTest "setfacl recursive functionality"

    rlRun "setfacl -R -m u:root:rw- testdir" 0 "recursiveset user ACL"

    output1=$(getfacl testdir/file1 2>&1)

    output2=$(getfacl testdir/subdir1/file2 2>&1)

    rlRun "echo \"\$output1\" | grep -q 'user:root:rw-'" 0 "verify file1 recursiveset ACL"

    rlRun "echo \"\$output2\" | grep -q 'user:root:rw-'" 0 "verify subdir1/file2 recursiveset ACL"



    rlRun "setfacl -R -b testdir" 0 "recursivedeleteall ACL"

    output1=$(getfacl testdir/file1 2>&1)

    output2=$(getfacl testdir/subdir1/file2 2>&1)

    rlRun "! echo \"\$output1\" | grep -q 'user:root:'" 0 "confirm file1 recursivedeletesuccess"

    rlRun "! echo \"\$output2\" | grep -q 'user:root:'" 0 "confirm subdir1/file2 recursivedeletesuccess"

    rlPhaseEnd



    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # acl Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

