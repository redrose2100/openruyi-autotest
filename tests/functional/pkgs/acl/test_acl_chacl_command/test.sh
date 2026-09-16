#!/bin/bash

# Functional test: acl - chacl command

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    aclSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlRun "touch testfile" 0 "Create test file"

    rlRun "mkdir testdir" 0 "Create test directory"

    rlRun "touch testdir/file1" 0 "createtestsubfile"

    rlPhaseEnd



    rlPhaseStartTest "chacl command functionality"

    rlRun "setfacl -b testfile" 0 "Cleanup ACL"

    rlRun "chacl -l testfile" 0 "use chacl view ACL"



    rlRun "chacl u::rw-,g::r--,o::r-- testfile" 0 "use chacl setbasic ACL"

    output=$(getfacl testfile 2>&1)

    rlRun "echo \"\$output\" | grep -q 'user::rw-'" 0 "confirm chacl set user ACL"



    rlRun "chacl -d u::rwx,g::r-x,o::r-x testdir" 0 "use chacl set default ACL"

    output=$(getfacl testdir 2>&1)

    rlRun "echo \"\$output\" | grep -q 'default:user::rwx'" 0 "confirm chacl -d set default ACL"



    rlRun "chacl -R u::rw-,g::r--,o::r--,m::r-- testdir" 0 "use chacl recursiveset ACL"

    output=$(getfacl testdir/file1 2>&1)

    rlRun "echo \"\$output\" | grep -q 'user::rw-'" 0 "confirm chacl -R recursivesetsuccess"



    rlRun "chacl -b u::rwx,g::r-x,o::r-x u::rwx,g::r-x,o::r-x testdir" 0 "use chacl -b simultaneouslyset"

    output=$(getfacl testdir 2>&1)

    rlRun "echo \"\$output\" | grep -q 'default:user::rwx'" 0 "confirm chacl -b simultaneouslyset access+default"

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

