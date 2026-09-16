#!/bin/bash

# Functional test: acl - special cases

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

    rlPhaseEnd



    rlPhaseStartTest "special scenarios"

    rlRun "setfacl -m u:root:rwx,u:daemon:r-x,g:root:r--,g:wheel:rw- testfile" 0 "setmultiuserandgroup ACL"

    output=$(getfacl testfile 2>&1)

    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "confirm user:root:rwx alreadyset"

    rlRun "echo \"\$output\" | grep -q 'user:daemon:r-x'" 0 "confirm user:daemon:r-x alreadyset"

    rlRun "echo \"\$output\" | grep -q 'group:root:r--'" 0 "confirm group:root:r-- alreadyset"

    rlRun "echo \"\$output\" | grep -q 'group:wheel:rw-'" 0 "confirm group:wheel:rw- alreadyset"



    rlRun "setfacl -m u:root:rwx,g:root:rwx testfile" 0 "settest ACL"

    rlRun "getfacl -R testdir > acl_backup.txt" 0 "export ACL "

    rlRun "setfacl -b testfile" 0 " ACL"

    rlRun "setfacl --restore acl_backup.txt" 0 "retry ACL"



    rlRun "setfacl --test -m u:root:rwx testfile" 0 "use --test modenoactual"

    rlRun "getfacl testfile" 0 "verify --test modenot ACL"

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

