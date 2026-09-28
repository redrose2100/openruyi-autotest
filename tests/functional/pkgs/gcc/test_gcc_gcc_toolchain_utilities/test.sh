#!/bin/bash
# Functional test: gcc - GCC-toolchain-utilities
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "GCC-toolchain-utilities"
    rlRun "gcc-ar --version" 0 "gcc-ar version check"
    rlRun "gcc-nm --version" 0 "gcc-nm version check"
    rlRun "gcc-ranlib --version" 0 "gcc-ranlib version check"
    rlRun "gcov-dump --version" 0 "gcov-dump version check"
    rlRun "gcov-tool --version" 0 "gcov-tool version check"
    rlRun "lto-dump --version" 0 "lto-dump version check"
    rlRun "cc --version" 0 "cc version check"
    rlRun "test \"$(cc --version 2>&1 | head -1)\" = \"$(gcc --version 2>&1 | head -1)\"" 0 "cc equals gcc"
    rlRun "c++ --version" 0 "c++ version check"
    rlRun "test \"$(c++ --version 2>&1 | head -1)\" = \"$(g++ --version 2>&1 | head -1)\"" 0 "c++ equals g++"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # gcc Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd

# pkgs-full-test-run v1
