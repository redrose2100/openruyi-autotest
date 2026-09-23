#!/bin/bash
# Functional test: gcc - Compiler-optimization-flags
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo '#include <stdio.h>
int main() { printf(\"Hello\\n\"); return 0; }' > hello.c" 0 "Create hello.c"
    rlRun "echo 'int compute(int n) { int s=0; for(int i=0;i<n;i++) s+=i; return s; }
int main() { return compute(100); }' > compute.c" 0 "Create compute.c"
    rlPhaseEnd

    rlPhaseStartTest "Compiler-optimization-flags"
    rlRun "gcc -O0 compute.c -o compute_O0" 0 "Compile with -O0"
    rlRun "gcc -O2 compute.c -o compute_O2" 0 "Compile with -O2"
    rlRun "gcc -g hello.c -o hello_dbg" 0 "Compile with debug symbols -g"
    rlRun "file hello_dbg | grep -q \"debug_info\"" 0 "Verify debug symbols present"
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
