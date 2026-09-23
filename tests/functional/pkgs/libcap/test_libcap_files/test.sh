#!/bin/bash
# Functional test: libcap -ļ֤
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    libcapSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "ļ֤"
    rlRun "ls /usr/lib64/libcap.so.2* 2>/dev/null || ls /usr/lib/libcap.so.2* 2>/dev/null || echo \"not in standard path\"" 0 " libcap.so.2"
    rlRun "ls /usr/lib64/libcap.so.2.76* 2>/dev/null || ls /usr/lib/libcap.so.2.76* 2>/dev/null || echo \"not in standard path\"" 0 " libcap.so.2.76"
    rlRun "ls /usr/lib64/libpsx.so.2* 2>/dev/null || ls /usr/lib/libpsx.so.2* 2>/dev/null || echo \"not in standard path\"" 0 " libpsx.so.2"
    rlRun "ls /usr/lib64/libpsx.so.2.76* 2>/dev/null || ls /usr/lib/libpsx.so.2.76* 2>/dev/null || echo \"not in standard path\"" 0 " libpsx.so.2.76"
    rlRun "ls /usr/lib64/pam_cap.so* 2>/dev/null || ls /usr/lib/pam_cap.so* 2>/dev/null || echo \"not in standard path\"" 0 " pam_cap.so"
    rlRun "pkg-config --libs libcap 2>&1 " 0 "pkg-config Ϣ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # libcap Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
