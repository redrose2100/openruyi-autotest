#!/bin/bash

# Functional test: lvm2 - lvm2 error handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    lvm2Setup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "lvm2 error handling"

    rlRun "lvm version 2>&1 " 0 "LVM "

    rlRun "lvm help 2>&1 | head -10" 0 "Display first lines"

    rlRun "pvs 2>&1 " 0 "ʾerror handling"

    rlRun "vgs 2>&1 " 0 "ʾ"

    rlRun "lvs 2>&1 " 0 "ʾ߼"

    rlRun "pvdisplay 2>&1 " 0 "error handling"

    rlRun "vgdisplay 2>&1 " 0 "error handling"

    rlRun "lvdisplay 2>&1 " 0 "߼error handling"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # lvm2 Package managed by lib.sh 's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

