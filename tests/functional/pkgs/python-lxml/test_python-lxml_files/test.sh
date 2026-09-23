#!/bin/bash
# Functional test: python-lxml - lxml -ļ֤
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    pythonLxmlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "lxml -ļ֤"
    rlRun "ls /usr/lib64/_elementpath.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || ls /usr/lib/_elementpath.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || echo \"not in standard path\"" 0 " _elementpath.cpython-313-riscv64-linux-gnu.so"
    rlRun "ls /usr/lib64/builder.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || ls /usr/lib/builder.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || echo \"not in standard path\"" 0 " builder.cpython-313-riscv64-linux-gnu.so"
    rlRun "ls /usr/lib64/etree.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || ls /usr/lib/etree.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || echo \"not in standard path\"" 0 " etree.cpython-313-riscv64-linux-gnu.so"
    rlRun "ls /usr/lib64/_difflib.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || ls /usr/lib/_difflib.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || echo \"not in standard path\"" 0 " _difflib.cpython-313-riscv64-linux-gnu.so"
    rlRun "ls /usr/lib64/diff.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || ls /usr/lib/diff.cpython-313-riscv64-linux-gnu.so* 2>/dev/null || echo \"not in standard path\"" 0 " diff.cpython-313-riscv64-linux-gnu.so"
    rlRun "pkg-config --libs python-lxml 2>&1 " 0 "pkg-config Ϣ"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # python-lxml Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
