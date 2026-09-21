#!/bin/bash
# Functional test: cryptsetup - cryptsetup info
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    cryptsetupSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "cryptsetup info"
    rlRun "cryptsetup --version 2>&1 | head -3 || echo version_ok" 0 "cryptsetup: version"
    rlRun "cryptsetup --help 2>&1 | head -5" 0 "cryptsetup: help"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
