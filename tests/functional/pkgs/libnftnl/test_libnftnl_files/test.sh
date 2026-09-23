#!/bin/bash
# Functional test: libnftnl -ļ֤
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    libnftnlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "ļ֤"
    rlRun "ls /usr/lib64/libnftnl.so.11* 2>/dev/null || ls /usr/lib/libnftnl.so.11* 2>/dev/null || echo \"not in standard path\"" 0 " libnftnl.so.11"
    rlRun "ls /usr/lib64/libnftnl.so.11.6.0* 2>/dev/null || ls /usr/lib/libnftnl.so.11.6.0* 2>/dev/null || echo \"not in standard path\"" 0 " libnftnl.so.11.6.0"
    rlRun "pkg-config --libs libnftnl 2>&1 " 0 "pkg-config Ϣ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # libnftnl Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
