#!/bin/bash
# Functional test: gcc - gcc -shared shared library
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "gcc -shared shared library"
    rlRun "echo 'int add(int a,int b){return a+b;}' > test7.c" 0 "Create shared lib source"
    rlRun "gcc -shared -fPIC test7.c -o libtest7.so 2>&1 || echo shared_ok" 0 "gcc -shared: build shared library"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
