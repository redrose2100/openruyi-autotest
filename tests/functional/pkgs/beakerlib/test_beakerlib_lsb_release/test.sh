#!/bin/bash
# Functional test: beakerlib - lsb_release command
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -v - Show LSB Version"
        rlRun "beakerlib-lsb_release -v | grep 'LSB Version:'" 0 "lsb_release -v shows LSB Version"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -i - Show Distributor ID"
        rlRun "beakerlib-lsb_release -i | grep 'Distributor ID:'" 0 "lsb_release -i shows Distributor ID"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -d - Show Description"
        rlRun "beakerlib-lsb_release -d | grep 'Description:'" 0 "lsb_release -d shows Description"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -r - Show Release"
        rlRun "beakerlib-lsb_release -r | grep 'Release:'" 0 "lsb_release -r shows Release"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -c - Show Codename"
        rlRun "beakerlib-lsb_release -c | grep 'Codename:'" 0 "lsb_release -c shows Codename"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -s - Short output"
        rlRun "beakerlib-lsb_release -s" 0 "lsb_release -s executes successfully"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -a - Show all information"
        rlRun "beakerlib-lsb_release -a" 0 "lsb_release -a executes successfully"
    rlPhaseEnd

    rlPhaseStartTest "lsb_release -h - Show help"
        rlRun "beakerlib-lsb_release -h 2>&1 | grep -i 'Usage'" 0 "lsb_release -h shows Usage"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd