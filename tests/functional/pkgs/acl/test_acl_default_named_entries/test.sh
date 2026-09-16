#!/bin/bash

# Functional test: acl - default ACL with named user/group entries
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
    rlPhaseEnd

    rlPhaseStartTest "default ACL named entries"

    # Named user + named group in the default ACL of a directory
    rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x,d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set default ACL with named user and group entries"

    output=$(getfacl testdir 2>&1)
    rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "default user root entry set"
    rlRun "echo \"\$output\" | grep -q 'default:user:daemon:r-x'" 0 "default user daemon entry set"
    rlRun "echo \"\$output\" | grep -q 'default:group:root:r-x'" 0 "default group root entry set"
    rlRun "echo \"\$output\" | grep -q 'default:group:wheel:r--'" 0 "default group wheel entry set"

    # Newly created file inherits named user/group default entries
    rlRun "touch testdir/newfile" 0 "create new file in dir"
    output=$(getfacl testdir/newfile 2>&1)
    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "file inherits default user root"
    rlRun "echo \"\$output\" | grep -q 'user:daemon:r-x'" 0 "file inherits default user daemon"
    rlRun "echo \"\$output\" | grep -q 'group:root:r-x'" 0 "file inherits default group root"
    rlRun "echo \"\$output\" | grep -q 'group:wheel:r--'" 0 "file inherits default group wheel"

    # Newly created subdirectory inherits the default entries AND keeps them as default
    rlRun "mkdir testdir/newsubdir" 0 "create new subdir in dir"
    output=$(getfacl testdir/newsubdir 2>&1)
    rlRun "echo \"\$output\" | grep -q 'default:user:daemon:r-x'" 0 "subdir inherits default user daemon as default entry"
    rlRun "echo \"\$output\" | grep -q 'default:group:wheel:r--'" 0 "subdir inherits default group wheel as default entry"

    # setfacl -x removes a named user entry from the default ACL
    rlRun "setfacl -x d:u:daemon testdir" 0 "remove named user from default ACL"
    output=$(getfacl testdir 2>&1)
    rlRun "! echo \"\$output\" | grep -q 'default:user:daemon:'" 0 "default user daemon entry removed"
    rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "other default entries preserved"

    # setfacl -x removes a named group entry from the default ACL
    rlRun "setfacl -x d:g:wheel testdir" 0 "remove named group from default ACL"
    output=$(getfacl testdir 2>&1)
    rlRun "! echo \"\$output\" | grep -q 'default:group:wheel:'" 0 "default group wheel entry removed"

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
