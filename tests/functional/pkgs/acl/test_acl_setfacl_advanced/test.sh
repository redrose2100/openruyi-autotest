#!/bin/bash

# Functional test: acl - setfacl advanced

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



    rlPhaseStartTest "setfacl advanced functionality"

    rlRun "setfacl -m d:u:root:rwx testdir" 0 "isdirectoryset default user ACL"

    rlRun "getfacl testdir" 0 "verify default ACL set"

    rlRun "getfacl testdir | grep -q 'default:user:root:rwx'" 0 "confirm default:user:root:rwx alreadyset"



    rlRun "setfacl -m d:g:root:r-x testdir" 0 "isdirectoryset default group ACL"

    rlRun "getfacl testdir" 0 "verify default group ACL"



    rlRun "setfacl -m d:m::rwx testdir" 0 "isdirectoryset default mask"

    rlRun "getfacl testdir" 0 "verify default mask"



    rlRun "setfacl -m d:o::r-- testdir" 0 "isdirectoryset default other"

    rlRun "getfacl testdir" 0 "verify default other"



    rlRun "setfacl --set u::rw-,u:root:rwx,g::r--,o::r--,m::rwx testfile" 0 "use --set replaceint ACL"

    rlRun "getfacl testfile" 0 "verify ACL replace"

    rlRun "getfacl testfile | grep -q 'user:root:rwx'" 0 "confirm --set alreadyreplace ACL"



    rlRun "echo 'u:root:rw-' > acl_rules.txt" 0 "create ACL file"

    rlRun "setfacl -M acl_rules.txt testfile" 0 "fromfilereadandshouldwith ACL"

    rlRun "getfacl testfile" 0 "verifyfromfileshouldwith ACL"

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

