#!/bin/bash
# Functional test: acl - chacl recursive and extended options (-R, -D, -B, -l, -r)

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        uid=$(whoami)
        touch f
        mkdir -p dir/subdir
        touch f-R f-l dir/subfile
        rlRun "setfacl -m user:${uid}:rwx f-R" 0 "Set ACL on f-R"
        rlRun "setfacl -d -m user:${uid}:rwx dir" 0 "Set default ACL on dir"
    rlPhaseEnd

    rlPhaseStartTest "chacl -R (remove ACL)"
        rlRun "getfacl f-R | grep -q '^user:$uid:rwx'" 0 "ACL exists before -R"
        rlRun "chacl -R f-R" 0 "Remove ACL via chacl -R"
        rlRun "getfacl f-R | grep -c '^user:$uid:' | grep -q 0" 0 "Named user ACL removed"
        rlRun "getfacl f-R | grep -c '^mask:' | grep -q 0" 0 "Mask ACL removed"
    rlPhaseEnd

    rlPhaseStartTest "chacl -D (remove default ACL)"
        rlRun "getfacl dir | grep -c '^default' | grep -q 5" 0 "Default ACL entries exist"
        rlRun "chacl -D dir" 0 "Remove default ACL via chacl -D"
        rlRun "getfacl dir | grep -c '^default' | grep -q 0" 0 "Default ACL entries removed"
    rlPhaseEnd

    rlPhaseStartTest "chacl -B (restore base ACL)"
        rlRun "chacl u::rwx,g::r-x,o::r--,m::r-x f" 0 "Set ACL first"
        rlRun "chacl -B f" 0 "Restore base ACL via chacl -B"
        rlRun "getfacl f | grep -q '^user::rw-'" 0 "Base user ACL restored"
        rlRun "getfacl f | grep -q '^group::r--'" 0 "Base group ACL restored"
        rlRun "getfacl f | grep -q '^other::r--'" 0 "Base other ACL restored"
    rlPhaseEnd

    rlPhaseStartTest "chacl -l (list ACL)"
        rlRun "chacl -l f-l | grep -qE '^f-l \[u::rw-,g::r--,o::r--\]'" 0 "List ACL via chacl -l"
    rlPhaseEnd

    rlPhaseStartTest "chacl -r (recursive set)"
        rlRun "getfacl dir/subfile | grep -c '^mask:' | grep -q 0" 0 "No mask ACL on subfile before -r"
        rlRun "chacl -r u::rwx,g::r-x,o::r--,m::rx dir" 0 "Recursive set via chacl -r"
        rlRun "getfacl dir/subfile | grep -q '^mask::r-x'" 0 "Mask ACL propagated to subfile"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd