#!/bin/bash
# Functional test: gdb - backtrace and register inspection
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y gdb gcc 2>/dev/null
        cat > test.c << 'CEOF'
#include <stdio.h>
int add(int a, int b) { return a + b; }
int main() {
    int sum[10], i;
    int array1[10] = {48,56,77,33,33,11,226,544,78,90};
    int array2[10] = {85,99,66,0x199,393,11,1,2,3,4};
    for (i = 0; i < 10; i++) { sum[i] = add(array1[i], array2[i]); }
    return 0;
}
CEOF
        rlRun "gcc test.c -g -o test" 0 "Compile test program"
    rlPhaseEnd

    rlPhaseStartTest "gdb backtrace: start, bt, bt full, info frame, info registers"
        gdb ./test << 'GDBEOF' > gdb.log 2>&1
start
bt
bt full
info f
info registers
q
GDBEOF
        # Verify stack frame keywords appear
        rlRun "grep -qiE 'main|stack|frame' gdb.log" 0 "gdb backtrace shows stack frames"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd