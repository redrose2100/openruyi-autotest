#!/bin/bash

# Functional test: acl - getfacl backup / setfacl --restore standard usage
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

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

    rlPhaseStartTest "setfacl backup and restore"

    # Prepare a known ACL state: access entries + default entries
    rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "set access ACL on file"
    rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x testdir" 0 "set default ACL on directory"

    # getfacl output is the machine-readable backup format used by
    # setfacl --restore (setfacl itself has no --backup option)
    rlRun "getfacl testfile > acl.backup" 0 "getfacl backup file ACL"
    rlRun "test -f acl.backup" 0 "backup file created"
    rlRun "grep -q '^# file:' acl.backup" 0 "backup file contains file header"

    # --restore applies the backup back
    rlRun "setfacl -b testfile" 0 "clear all ACL entries before restore"
    rlRun "setfacl --restore=acl.backup" 0 "setfacl --restore file ACL"
    output=$(getfacl testfile 2>&1)
    rlRun "echo \"\$output\" | grep -q 'user:root:rwx'" 0 "restore re-adds user:root:rwx"
    rlRun "echo \"\$output\" | grep -q 'group:root:r-x'" 0 "restore re-adds group:root:r-x"

    # getfacl shows default entries with 'default:' prefix; filter instead of -d flag
    rlRun "getfacl testdir 2>&1 | grep 'default:' > out_default.txt" 0 "get default ACL entries"
    rlRun "grep -q 'default:user:root:rwx' out_default.txt" 0 "default user entry present"
    rlRun "grep -q 'default:group:root:r-x' out_default.txt" 0 "default group entry present"

    # Restoring a directory backup also restores its default entries
    rlRun "getfacl testdir > dir.backup" 0 "getfacl backup dir ACL"
    rlRun "setfacl -k testdir" 0 "clear default ACL entries before restore"
    # setfacl --restore reads '# file:' line from backup to locate the path
    rlRun "cd $TmpDir && setfacl --restore=dir.backup" 0 "setfacl --restore dir ACL"
    output=$(getfacl testdir 2>&1)
    rlRun "echo \"\$output\" | grep -q 'default:user:root:rwx'" 0 "dir restore re-adds default user entry"
    rlRun "echo \"\$output\" | grep -q 'default:group:root:r-x'" 0 "dir restore re-adds default group entry"

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
