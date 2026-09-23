#!/bin/bash
# Functional test: gcc - Basic-C-compilation
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

    rlPhaseStartTest "Basic-C-compilation"
    rlRun "gcc hello.c -o hello" 0 "Compile hello.c to hello"
    rlRun "./hello" 0 "Run compiled hello"
    rlRun "file hello | grep -i elf" 0 "Verify output is ELF binary"
    rlRun "gcc -o myhello hello.c" 0 "Compile with -o flag"
    rlRun "./myhello" 0 "Run myhello"
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
