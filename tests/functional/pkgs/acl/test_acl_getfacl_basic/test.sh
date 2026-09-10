#!/bin/bash

# Functional test: acl - getfacl basic

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



    rlPhaseStartTest "getfacl basic functionality"

    # Save getfacl output to files for rlAssertGrep/rlAssertNotGrep,
    # which expect a file path (not inline content) as second argument.

    # test 1.1: view file default ACL

    rlRun "getfacl testfile > out_getfacl.txt 2>&1" 0 "getfacl testfile produces output"

    rlAssertGrep "user::" out_getfacl.txt

    rlAssertGrep "group::" out_getfacl.txt

    rlAssertGrep "other::" out_getfacl.txt

    # test 1.2: view directory default ACL

    rlRun "getfacl testdir > out_getfacl_dir.txt 2>&1" 0 "getfacl testdir produces output"

    rlAssertGrep "user::" out_getfacl_dir.txt

    rlAssertGrep "group::" out_getfacl_dir.txt

    # test 1.3: use -a parameter only display access ACL

    rlRun "getfacl -a testfile > out_getfacl_a.txt 2>&1" 0 "use -a parameter view access ACL"

    rlAssertGrep "user::" out_getfacl_a.txt



    # test 1.3.1: use -a parameter output must NOT contain default entries

    if getfacl -a testfile 2>&1 | grep -q "default:"; then

        rlFail "use -a parameter output contains default entries"

    else

        rlPass "use -a parameter output contains no default entries"

    fi



    # test 1.4: set default ACL and verify with plain getfacl
    # (getfacl -d only shows the access ACL; the default ACL
    # entries are shown by plain getfacl after setfacl -m d:*)

    rlRun "setfacl -m d:u::rwx,d:g::r-x,d:o::--- testdir" 0 "set default ACL on testdir"

    rlRun "getfacl testdir > out_getfacl_plain.txt 2>&1" 0 "getfacl testdir with default ACL"

    rlAssertGrep "default:user::rwx" out_getfacl_plain.txt

    rlAssertGrep "default:group::r-x" out_getfacl_plain.txt

    rlAssertGrep "default:other::---" out_getfacl_plain.txt

    # test 1.5: use -c parameter no display header

    rlRun "getfacl -c testfile > out_getfacl_c.txt 2>&1" 0 "use -c parameter no display header"

    rlAssertNotGrep "^# file:" out_getfacl_c.txt

    # test 1.6: use -n parameter display number user/group ID

    rlRun "getfacl -n testfile > out_getfacl_n.txt 2>&1" 0 "use -n parameter display number ID"

    rlAssertGrep "[0-9]" out_getfacl_n.txt

    # test 1.7: use -t parameter use output format

    rlRun "getfacl -t testfile > out_getfacl_t.txt 2>&1" 0 "use -t parameter output format"

    rlAssertGrep "[r-][w-][x-]" out_getfacl_t.txt

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

