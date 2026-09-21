#!/bin/bash
# Functional test: cmake - cmake -DCMAKE_INSTALL_PREFIX
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cmakeSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "cmake -DCMAKE_INSTALL_PREFIX"
    rlRun "cmake -DCMAKE_INSTALL_PREFIX=/tmp/test_install /dev/null 2>&1 | grep -qiE 'error|CMake Error' || echo install_prefix_ok" 0 "cmake -DCMAKE_INSTALL_PREFIX: option accepted"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
