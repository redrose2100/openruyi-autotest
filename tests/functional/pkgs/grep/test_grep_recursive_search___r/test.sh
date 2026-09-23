#!/bin/bash
# Functional test: grep - Recursive-search---r
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    grepSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "mkdir -p subdir" 0 "Create subdir"
    rlRun "echo 'nested content hello world' > subdir/file1.txt" 0 "Create file1 in subdir"
    rlRun "echo 'hello from subdir' > subdir/file2.txt" 0 "Create file2 in subdir"
    rlRun "echo 'hello no match' > topfile.txt" 0 "Create top-level test file"
    rlPhaseEnd

    rlPhaseStartTest "Recursive-search---r"
    rlRun "grep -r nested subdir/" 0 "Recursive grep in subdirectory"
    rlRun "grep -rl hello subdir/" 0 "Recursive list files with matches"
    rlRun "grep -r --include=\"*.txt\" hello ." 0 "Recursive with --include filter"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # grep Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
