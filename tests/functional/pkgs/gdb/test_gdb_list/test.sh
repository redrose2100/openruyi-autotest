#!/bin/bash
# Functional test: gdb - list source and disassemble
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # openruyi's repo needs --nogpgcheck --setopt=sslverify=0, otherwise dnf
        # fails with "NOKEY" and gdb is never installed. The CI test environment
        # only pre-installs gcc, so install gdb here.
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y \
            --nogpgcheck --setopt=sslverify=0 gdb gcc 2>&1 | tail -3
        rlRun "command -v gdb" 0 "gdb is available"
        cat > add.c << 'CEOF'
#include <stdio.h>
int add(int x, int y) { return x + y; }
int main() {
    int x = 10, y = 20, num = add(x, y);
    printf("num=%d\n", num);
    return 0;
}
CEOF
        rlRun "gcc -g add.c -o a.out" 0 "Compile test program"
    rlPhaseEnd

    rlPhaseStartTest "gdb list and disassemble"
        gdb -batch -ex 'list 4' -ex 'list main' -ex 'disassemble add' -ex 'disassemble main' ./a.out > gdb.log 2>&1
        rlRun "grep -q 'int add' gdb.log" 0 "gdb list shows source lines"
        rlRun "grep -qE '0x[0-9a-f]+' gdb.log" 0 "gdb disassemble shows assembly addresses"
        rlRun "grep -qiE '<(add|main)>:' gdb.log" 0 "gdb disassemble names the function"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd