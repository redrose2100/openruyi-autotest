#!/bin/bash
# Functional test: acl - setfacl - error on nonexistent file
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "setfacl on nonexistent file fails"
        rlRun "setfacl -m u:root:rwx nonexistent_file" 1-255 "setfacl on nonexistent file fails"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
