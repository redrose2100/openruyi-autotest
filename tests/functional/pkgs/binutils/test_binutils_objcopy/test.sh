#!/bin/bash
# Functional test: binutils - objcopy
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "objcopy"
    rlRun "TmpDir=$(mktemp -d)" 0 "error handlingʱĿ¼"
    rlRun "cd $TmpDir" 0 "error handlingdirectory"
    rlRun "cp /usr/bin/ls ." 0 "List files"
    rlRun "objcopy --help 2>&1 | head -10" 0 "Copy and convert object files"
    rlRun "strip --help 2>&1 | head -10" 0 "Strip symbols from binary"
    rlRun "strip ls 2>&1 " 0 "strip ļ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # binutils Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
