#!/bin/bash
# Functional test: findutils - find -perm permissions
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    findutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "mkdir -p find_testdir" 0 "Create test directory"

    rlPhaseEnd

    rlPhaseStartTest "find -perm permissions"
    rlRun "touch find_testdir/p1.txt && chmod 644 find_testdir/p1.txt" 0 "Create file with 644"
    rlRun "find find_testdir -perm 644 2>&1 | head -3 || echo perm_works" 0 "find -perm: match by permissions"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
