#!/bin/bash

# Functional test: acl - setfacl remove

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

    # pre ACL deletetestuse

    rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "pre ACL deletetest"

    rlPhaseEnd



    rlPhaseStartTest "setfacl delete functionality"

    rlRun "setfacl -x u:root testfile" 0 "deleteuser root ACL entries"

    output=$(getfacl testfile 2>&1)

    rlRun "! echo \"\$output\" | grep -q 'user:root:'" 0 "confirmuser root entriesalreadydelete"



    rlRun "setfacl -x g:root testfile" 0 "deletegroup root ACL entries"

    output=$(getfacl testfile 2>&1)

    rlRun "! echo \"\$output\" | grep -q 'group:root:'" 0 "confirmgroup root entriesalreadydelete"



    rlRun "setfacl -b testfile" 0 "deleteall ACL"

    output=$(getfacl testfile 2>&1)

    rlRun "! echo \"\$output\" | grep -q 'user:root:'" 0 "confirm -b postno ACL"



    rlRun "setfacl -k testdir" 0 "deletedirectory default ACL"

    output=$(getfacl testdir 2>&1)

    rlRun "! echo \"\$output\" | grep -q 'default:'" 0 "confirm -k postno default ACL"



    rlRun "echo 'u:root' > remove_rules.txt" 0 "createdeletefile"

    rlRun "setfacl -m u:root:rwx testfile" 0 "adduser ACL"

    rlRun "setfacl -X remove_rules.txt testfile" 0 "fromfilereadanddelete ACL"

    output=$(getfacl testfile 2>&1)

    rlRun "! echo \"\$output\" | grep -q 'user:root:'" 0 "confirmfromfiledeletesuccess"

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

