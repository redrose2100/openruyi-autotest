#!/bin/bash
# Functional test: gdb - backtrace and register inspection
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
        # -batch makes gdb exit after the last -ex command, which is far more
        # deterministic than feeding an interactive session via a heredoc.
        gdb -batch -ex 'start' -ex 'bt' -ex 'bt full' -ex 'info frame' -ex 'info registers' ./test > gdb.log 2>&1
        rlRun "grep -q '#0' gdb.log" 0 "gdb backtrace shows stack frame #0"
        rlRun "grep -q 'main' gdb.log" 0 "gdb backtrace shows main frame"
        rlRun "grep -qiE 'rax|eax|rip|pc' gdb.log" 0 "info registers shows register values"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd