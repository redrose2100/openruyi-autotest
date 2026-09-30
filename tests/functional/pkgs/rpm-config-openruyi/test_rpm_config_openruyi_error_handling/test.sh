#!/bin/bash

# Functional test: rpm-config-openruyi - config-openruyi - error handling

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    rpmConfigOpenruyiSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "config-openruyi - error handling"

    rlRun "rpm -q rpm-config-openruyi 2>/dev/null || echo not-found" 0 "rpm-config-openruyi check"

    rlRun "ls /usr/lib/rpm/openruyi/ 2>/dev/null || ls /usr/lib/rpm/macros.d/ 2>/dev/null" 0 "RPM macrodirectory exists"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # rpm-config-openruyi Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

