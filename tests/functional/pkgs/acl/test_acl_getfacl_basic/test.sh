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

    # test 1.1: viewfiledefault ACL

    rlRun "getfacl testfile 2>&1 | grep -qE \"user::|group::|other::\"" 0 "viewfiledefault ACL contains permissionentries"



    # test 1.2: viewdirectorydefault ACL

    rlRun "getfacl testdir 2>&1 | grep -qE \"user::|group::|other::\"" 0 "viewdirectorydefault ACL contains permissionentries"



    # test 1.3: use -a parameteronlydisplay access ACL

    rlRun "getfacl -a testfile 2>&1 | grep -qE \"user::|group::\"" 0 "use -a parameterview access ACL"

    rlAssertGrep "user::" "$(getfacl -a testfile 2>&1)" "-a outputcontains access ACL entries"



    # test 1.4: use -d parameteronlydisplay default ACL

    rlRun "getfacl -d testfile 2>&1 | grep -qE \"user::|default\"" 0 "use -d parameterview default ACL contains default entries"

    # test 1.4.1: use -a parameter output must NOT contain default entries

    if getfacl -a testfile 2>&1 | grep -q "default:"; then

    rlFail "use -a parameter output contains default entries"

    else

    rlPass "use -a parameter output contains no default entries"

    fi



    # test 1.5: use -c parameternodisplayheader

    rlRun "getfacl -c testfile 2>&1" 0 "use -c parameternodisplayheader"

    rlAssertNotGrep "^# file:" "$(getfacl -c testfile 2>&1)" "-c outputnocontainsheader"



    # test 1.6: use -n parameterdisplaynumberuser/group ID

    rlRun "getfacl -n testfile 2>&1 | grep -qE \"[0-9]+\"" 0 "use -n parameterdisplaynumber ID"



    # test 1.7: use -t parameteruseoutputformat

    rlRun "getfacl -t testfile 2>&1 | grep -qE \"[r-][w-][x-]\"" 0 "use -t parameteroutputcontains permission"

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

