#!/bin/bash
# Functional test: acl - setfacl - set default other on directory
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "set default other on directory"
        rlRun "setfacl -m d:o::r-- testdir" 0 "set default other"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "verify" 
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
