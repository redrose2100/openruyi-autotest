#!/bin/bash

# Functional test: krb5 - krb5 error handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    krb5Setup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "krb5 error handling"

    rlRun "klist 2>&1 " 0 "Ʊ(Ϊ)"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # krb5 Package managed by lib.sh 's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

