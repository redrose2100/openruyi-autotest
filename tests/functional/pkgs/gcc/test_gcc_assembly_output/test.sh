#!/bin/bash
# Functional test: gcc - Assembly-output
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
    rlPhaseEnd

    rlPhaseStartTest "Assembly-output"
    rlRun "gcc -S hello.c -o hello.s" 0 "Generate assembly with -S"
    rlRun "grep -q \"main:\" hello.s" 0 "Check main label in assembly"
    rlRun "as hello.s -o hello_obj.o" 0 "Assemble to object file"
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
