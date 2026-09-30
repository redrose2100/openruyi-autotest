#!/bin/bash


# Functional test: attr - error handling


# Beakerlib-based test with lifecycle management


# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)





. /usr/share/beakerlib/beakerlib.sh || exit 1


. "$(dirname "$0")/../lib.sh"





rlJournalStart


    rlPhaseStartSetup "Environment setup"


    attrSetup


    TmpDir=$(mktemp -d)


    rlRun "cd $TmpDir" 0 "Enter temporary test directory"


    rlPhaseEnd





    rlPhaseStartTest "error handling"


    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingdirectory"


    rlRun "cd $TmpDir" 0 "error handlingdirectory"


    rlRun "getfattr nonexistent_file" 1-255 "Unable togeterror handlingfileattribute"


    rlRun "setfattr -n user.test -v val nonexistent_file" 1-255 "Invalid option error handling"


    rlRun "getfattr --invalid-flag nonexistent" 1-255 "error handlingInvalid option"


    rlPhaseEnd








    rlPhaseStartCleanup "Clean up test environment"


    rlRun "cd /" 0 "Leave test directory"


    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then


    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"


    fi


    # attr Package managed by lib.sh's reference counting auto-uninstall


    rlPhaseEnd





    rlJournalPrintText


rlJournalEnd


