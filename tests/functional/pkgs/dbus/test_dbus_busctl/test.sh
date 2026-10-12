#!/bin/bash
# Functional test: dbus - busctl command
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        bus=$(busctl list --unique 2>/dev/null | grep org.freedesktop.DBus | awk '{print $1}' | head -1)
        [ -z "$bus" ] && bus="org.freedesktop.DBus"
    rlPhaseEnd

    rlPhaseStartTest "busctl - list buses"
        rlRun "busctl | grep -E 'org\.freedesktop|\.bus'" 0 "busctl lists D-Bus buses"
    rlPhaseEnd

    rlPhaseStartTest "busctl status - show bus status"
        rlRun "busctl status 2>&1 | head -5" 0 "busctl status shows bus info"
    rlPhaseEnd

    rlPhaseStartTest "busctl tree - show object tree"
        rlRun "busctl tree $bus 2>&1 | head -5" 0 "busctl tree shows object hierarchy"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd