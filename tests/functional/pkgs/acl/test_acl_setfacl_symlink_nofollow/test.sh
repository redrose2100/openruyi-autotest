#!/bin/bash
# Functional test: acl - setfacl -P do not follow symlink
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
        rlRun "ln -s testfile symlink" 0 "create symlink" 
    rlPhaseEnd

    rlPhaseStartTest "use -P to not follow symlink"
        rlRun "setfacl -P -m u:root:r-- symlink" 0 "setfacl -P on symlink" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
