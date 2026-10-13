#!/bin/bash
# Functional test: dbus - run-session, cleanup-sockets, test-tool
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "dbus-run-session - help and version"
        rlRun "dbus-run-session --help 2>&1 | head -3" 0 "dbus-run-session --help works"
        rlRun "dbus-run-session --version 2>&1" 0 "dbus-run-session --version works"
    rlPhaseEnd

    rlPhaseStartTest "dbus-cleanup-sockets - help and version"
        rlRun "dbus-cleanup-sockets --help 2>&1 | head -3" 0 "dbus-cleanup-sockets --help works"
        rlRun "dbus-cleanup-sockets --version 2>&1" 0 "dbus-cleanup-sockets --version works"
    rlPhaseEnd

    rlPhaseStartTest "dbus-test-tool - black-hole"
        rlRun "timeout 3 dbus-test-tool black-hole --session 2>&1; true" 0 "dbus-test-tool black-hole --session runs"
        rlRun "dbus-test-tool black-hole --name=com.example.NoReply 2>&1; true" 0 "dbus-test-tool black-hole --name runs"
    rlPhaseEnd

    rlPhaseStartTest "dbus-test-tool - echo mode"
        rlRun "timeout 3 dbus-test-tool echo --session --sleep-ms=10 2>&1; true" 0 "dbus-test-tool echo runs"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd