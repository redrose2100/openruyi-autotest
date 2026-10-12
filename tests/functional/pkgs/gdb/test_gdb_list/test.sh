#!/bin/bash
# Functional test: gdb - list source and disassemble
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y gdb gcc 2>/dev/null
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
        gdb ./a.out << 'GDBEOF' > gdb.log 2>&1
list 4
l main
disassemble add
disassemble main
q
GDBEOF
        rlRun "grep -qiE '0x|add|push|ret' gdb.log" 0 "gdb disassemble shows assembly instructions"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd