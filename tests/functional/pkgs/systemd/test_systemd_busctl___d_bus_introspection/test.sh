#!/bin/bash
# Functional test: systemd - busctl---D-Bus-introspection
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    systemdSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "busctl---D-Bus-introspection"
    rlRun "busctl --version 2>&1 " 0 "busctl version"
    rlRun "busctl list 2>&1 | head -10" 0 "busctl list: list services"
    rlRun "busctl status 2>&1 | head -10" 0 "busctl status: bus status"
    rlRun "busctl tree org.freedesktop.systemd1 2>&1 | head -10" 0 "busctl tree: object tree"
    rlRun "busctl introspect org.freedesktop.systemd1 /org/freedesktop/systemd1 2>&1 | head -10" 0 "busctl introspect"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # systemd Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
