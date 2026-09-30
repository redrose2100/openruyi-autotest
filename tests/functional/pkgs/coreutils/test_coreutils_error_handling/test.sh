#!/bin/bash
# Functional test: coreutils - Error-handling
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "mkdir ls_testdir" 0 "Create test directory for error tests"
    rlRun "mkdir a" 0 "Create directory a"
    rlRun "touch a/f1" 0 "Create file in directory a"
    rlPhaseEnd

    rlPhaseStartTest "Error-handling"
    rlRun "cp nonexistent.txt /tmp/ 2>&1" 1 "cp: error on nonexistent source"
    rlRun "ls nonexistent_file 2>&1" 2 "ls: error on nonexistent file"
    rlRun "mkdir ls_testdir 2>&1" 1 "mkdir: error on existing dir"
    rlRun "rm ls_testdir 2>&1" 1 "rm: error on dir without -r"
    rlRun "rmdir a 2>&1" 1 "rmdir: error on non-empty dir"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # coreutils Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
