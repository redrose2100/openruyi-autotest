#!/bin/bash

# Functional test: acl - ACL permission verify

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

    rlPhaseEnd



    rlPhaseStartTest "ACL permission verification"

    rlRun "setfacl --set u::rwx,u:root:rwx,g::r-x,o::r--,m::rwx testfile" 0 "setfullpermission"

    output=$(getfacl testfile 2>&1)

    rlRun "echo \"\$output\" | grep -q 'user::rwx'" 0 "confirm user::rwx alreadyset"

    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "confirm user:root:rwx alreadyset"

    rlRun "echo \"\$output\" | grep -q 'group::r-x'" 0 "confirm group::r-x alreadyset"

    rlRun "echo \"\$output\" | grep -q 'mask::rwx'" 0 "confirm mask::rwx alreadyset"



    rlRun "setfacl -m u:root:rwx,m::r-- testfile" 0 "set mask haspermission"

    output=$(getfacl testfile 2>&1)

    rlRun "echo \"\$output\" | grep -q 'mask::r--'" 0 "confirm mask::r-- alreadyset"

    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "confirm user:root permission mask "

    # Effective permission check: with mask=r--, the named user root entry
    # is truncated to r--. getfacl -e prints the effective permissions.
    rlRun "getfacl -e testfile > out_effective.txt 2>&1" 0 "getfacl -e shows effective permissions"

    rlRun "grep -q 'user:root:rwx.*#effective:r--' out_effective.txt" 0 "mask r-- truncates user:root to effective r--"

    rlRun "grep -q 'group::r-x.*#effective:r--' out_effective.txt" 0 "mask r-- truncates group to effective r--"



    # After raising the mask back to rwx, the effective permissions are restored
    rlRun "setfacl -m m::rwx testfile" 0 "raise mask back to rwx"

    rlRun "getfacl -e testfile > out_effective2.txt 2>&1" 0 "getfacl -e after mask raise"

    rlRun "grep -q 'user:root:rwx.*#effective:rwx' out_effective2.txt" 0 "mask rwx restores effective rwx for user:root"

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

