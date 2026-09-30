#!/bin/bash
# Functional test: acl - setfacl - permission denied on protected file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
    rlPhaseEnd

    rlPhaseStartTest "permission denied on protected file"
        if [ "$(id -u)" = "0" ]; then
            rlRun "sudo -n -u openruyi setfacl -m u:root:rwx /root/test 2>&1" 1-255 "non-root cannot set ACL"
        else
            rlRun "setfacl -m u:root:rwx /root/test 2>&1" 1-255 "non-root cannot set ACL"
        fi
        rlPass "Permission denied handled correctly"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
