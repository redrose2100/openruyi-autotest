#!/bin/bash
# Functional test: util-linux - linux - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    utilLinuxSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "linux - version and help"
    rlRun "addpart --version 2>&1 " 0 "addpart version info"
    rlRun "addpart --help 2>&1 | head -5 || true" 0 "addpart help info"
    rlRun "agetty --version 2>&1 " 0 "agetty version info"
    rlRun "agetty --help 2>&1 | head -5 || true" 0 "agetty help info"
    rlRun "blkid --version 2>&1 " 0 "blkid version info"
    rlRun "blkid --help 2>&1 | head -5 || true" 0 "blkid help info"
    rlRun "blkdiscard --version 2>&1 " 0 "blkdiscard version info"
    rlRun "blkdiscard --help 2>&1 | head -5 || true" 0 "blkdiscard help info"
    rlRun "blockdev --version 2>&1 " 0 "blockdev version info"
    rlRun "blockdev --help 2>&1 | head -5 || true" 0 "blockdev help info"
    rlRun "cal --version 2>&1 " 0 "cal version info"
    rlRun "cal --help 2>&1 | head -5 || true" 0 "cal help info"
    rlRun "cfdisk --version 2>&1 " 0 "cfdisk version info"
    rlRun "cfdisk --help 2>&1 | head -5 || true" 0 "cfdisk help info"
    rlRun "chcpu --version 2>&1 " 0 "chcpu version info"
    rlRun "chcpu --help 2>&1 | head -5 || true" 0 "chcpu help info"
    rlRun "chfn --version 2>&1 " 0 "chfn version info"
    rlRun "chfn --help 2>&1 | head -5 || true" 0 "chfn help info"
    rlRun "chmem --version 2>&1 " 0 "chmem version info"
    rlRun "chmem --help 2>&1 | head -5 || true" 0 "chmem help info"
    rlRun "choom --version 2>&1 " 0 "choom version info"
    rlRun "choom --help 2>&1 | head -5 || true" 0 "choom help info"
    rlRun "chrt --version 2>&1 " 0 "chrt version info"
    rlRun "chrt --help 2>&1 | head -5 || true" 0 "chrt help info"
    rlRun "bits --version 2>&1 " 0 "bits version info"
    rlRun "bits --help 2>&1 | head -5 || true" 0 "bits help info"
    rlRun "blkpr --version 2>&1 " 0 "blkpr version info"
    rlRun "blkpr --help 2>&1 | head -5 || true" 0 "blkpr help info"
    rlRun "blkzone --version 2>&1 " 0 "blkzone version info"
    rlRun "blkzone --help 2>&1 | head -5 || true" 0 "blkzone help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # util-linux Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
