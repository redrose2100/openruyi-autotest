#!/bin/bash

# Functional test: openssh-clients - clients - Error-handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    opensshClientsSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "clients - Error-handling"

    rlRun "ssh -V 2>&1" 0 "ssh version info"

    rlRun "ssh -o ConnectTimeout=1 -o StrictHostKeyChecking=no nonexistent 2>&1" 255 "ssh connectiondoes not existshould error"

    rlRun "ssh-copy-id -h 2>&1 | grep -qi Usage" 0 "ssh-copy-id -h Show usage"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # openssh-clients Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

