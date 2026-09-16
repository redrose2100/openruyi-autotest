#!/bin/bash
# Functional test: acl - ACL inheritance
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    aclSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "mkdir testdir" 0 "Create test directory"
    rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x,d:o::r-- testdir" 0 "Set directory default ACL"
    rlPhaseEnd

    rlPhaseStartTest "ACL inheritance test"
    rlRun "touch testdir/newfile" 0 "Create new file in test directory"
    output=$(getfacl testdir/newfile 2>&1)
    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "New file inherits user default ACL"
    rlRun "echo \"\$output\" | grep -q 'group:root:r-x'" 0 "New file inherits group default ACL"

    rlRun "mkdir testdir/newsubdir" 0 "Create subdirectory in test directory"
    output=$(getfacl testdir/newsubdir 2>&1)
    rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "Subdirectory inherits default user ACL"
    rlRun "echo \"\$output\" | grep -q 'default:group:root:r-x'" 0 "Subdirectory inherits default group ACL"
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
