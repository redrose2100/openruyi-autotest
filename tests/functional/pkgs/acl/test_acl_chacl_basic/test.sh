#!/bin/bash
# Functional test: acl - chacl basic operations (no options, -b, -d)

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        uid=$(whoami)
        gid=$(id -gn)
        mkdir -p dir-b dir-d
        touch f f-l f-R dir/subfile
        rlRun "setfacl -d -m user::rwx dir-b" 0 "Set default ACL on dir-b"
        rlRun "setfacl -d -m user::rwx dir-d" 0 "Set default ACL on dir-d"
    rlPhaseEnd

    rlPhaseStartTest "chacl without options"
        # Basic ACL: set user::rw-, group::r--, other::r--
        rlRun "getfacl f | grep -qE '^user::rw-' && getfacl f | grep -qE '^group::r--' && getfacl f | grep -qE '^other::r--'" 0 "Verify base ACL on f"
        rlRun "chacl u::rwx,g::r-x,o::r--,u:$uid:r--,g:$gid:r--,m::r-x f" 0 "Apply ACL via chacl"
        rlRun "getfacl f | grep -q '^user::rwx'" 0 "Check user ACL applied"
        rlRun "getfacl f | grep -q '^group::r-x'" 0 "Check group ACL applied"
        rlRun "getfacl f | grep -q '^other::r--'" 0 "Check other ACL applied"
        rlRun "getfacl f | grep -q '^user:$uid:r--'" 0 "Check named user ACL applied"
        rlRun "getfacl f | grep -q '^mask::r-x'" 0 "Check mask ACL applied"
        rlRun "getfacl f | grep -q '^group:$gid:r--'" 0 "Check named group ACL applied"
    rlPhaseEnd

    rlPhaseStartTest "chacl -b (both access and default ACL)"
        rlRun "chacl -b u::rwx,g::r-x,o::r--,u:$uid:rwx,m::rw u::rwx,g::r-x,o::rwx,g:$gid:r--,m::r-x dir-b" 0 "Apply both ACLs via chacl -b"
        rlRun "getfacl dir-b | grep -q '^user:$uid:'" 0 "Access ACL named user exists"
        rlRun "getfacl dir-b | grep -q '^default:group:$gid:'" 0 "Default ACL named group exists"
    rlPhaseEnd

    rlPhaseStartTest "chacl -d (default ACL only)"
        rlRun "chacl -d u::rwx,g::r-x,o::rwx,g:$gid:r--,m::r-x dir-d" 0 "Apply default ACL via chacl -d"
        rlRun "getfacl dir-d | grep -q '^default:group:$gid:r--'" 0 "Default ACL group entry exists"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd