#!/bin/bash

# Functional test: acl - error handling

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



    rlPhaseStartTest "error handling"

    rlRun "getfacl nonexistent_file" 1-255 "testvsdoes not existfile getfacl error"

    rlRun "setfacl -m u:root:rwx nonexistent_file" 1-255 "testvsdoes not existfile setfacl error"



    rlRun "setfacl -m u:root:xyz testfile" 1-255 "testnopermissionerror"

    rlRun "setfacl -m x:root:rw testfile" 1-255 "testno ACL typeerror"



    rlRun "sudo -n -u openruyi setfacl -m u:root:rwx /root/test 2>&1" 1-255 "testpermissionnoerror"

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

