#!/bin/bash
# Functional test: gcc - Linking-and-libraries
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
    rlRun "echo '#include <math.h>
#include <stdio.h>
int main() { printf(\"%f\", sin(1.0)); return 0; }' > math_test.c" 0 "Create math_test.c"
    rlPhaseEnd

    rlPhaseStartTest "Linking-and-libraries"
    rlRun "gcc math_test.c -lm -o math_test" 0 "Link with -lm"
    rlRun "./math_test" 0 "Run math linked program"
    rlRun "gcc -static hello.c -o hello_static" 0 "Compile static binary"
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
