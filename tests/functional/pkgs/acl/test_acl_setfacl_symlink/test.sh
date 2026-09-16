#!/bin/bash

# Functional test: acl - setfacl symlink

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

    rlRun "ln -s testfile symlink" 0 "createsymbollink"

    rlPhaseEnd



    rlPhaseStartTest "setfacl symbollinkhandle"

    rlRun "setfacl -L -m u:root:rwx symlink" 0 "use -L symbollinkset ACL"

    output=$(getfacl testfile 2>&1)

    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "confirm -L symbollinksetsuccess"



    rlRun "setfacl -b testfile" 0 "Cleanup ACL"

    rlRun "setfacl -P -m u:root:r-- symlink" 0 "use -P nosymbollink"

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

