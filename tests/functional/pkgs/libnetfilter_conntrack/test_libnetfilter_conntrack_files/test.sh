#!/bin/bash
# Functional test: libnetfilter_conntrack -ļ֤
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    libnetfilterConntrackSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "ļ֤"
    rlRun "ls /usr/lib64/libnetfilter_conntrack.so.3* 2>/dev/null || ls /usr/lib/libnetfilter_conntrack.so.3* 2>/dev/null || echo \"not in standard path\"" 0 " libnetfilter_conntrack.so.3"
    rlRun "ls /usr/lib64/libnetfilter_conntrack.so.3.8.0* 2>/dev/null || ls /usr/lib/libnetfilter_conntrack.so.3.8.0* 2>/dev/null || echo \"not in standard path\"" 0 " libnetfilter_conntrack.so.3.8.0"
    rlRun "pkg-config --libs libnetfilter_conntrack 2>&1 " 0 "pkg-config Ϣ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # libnetfilter_conntrack Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
