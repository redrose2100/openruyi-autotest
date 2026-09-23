#!/bin/bash
# Functional test: gcc - Code-coverage--gcov
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo 'int main() { int x = 1; if (x) return 0; else return 1; }' > gcov_test.c" 0 "Create gcov_test.c"
    rlPhaseEnd

    rlPhaseStartTest "Code-coverage--gcov"
    rlRun "gcc -fprofile-arcs -ftest-coverage gcov_test.c -o gcov_test" 0 "Compile with coverage flags"
    rlRun "./gcov_test" 0 "Run coverage test program"
    rlRun "gcov gcov_test.c" 0 "Run gcov"
    rlRun "ls -la gcov_test.c.gcov" 0 "Check gcov output file exists"
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
