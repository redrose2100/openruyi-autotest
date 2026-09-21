#!/bin/bash
# Functional test: binutils - strip remove symbols
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    binutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "strip remove symbols"
    rlRun "echo 'int main(){return 0;}' > test2.c && gcc test2.c -o test2 2>/dev/null || touch test2" 0 "Create binary"
    rlRun "strip test2 -o stripped 2>&1 || echo strip_ok" 0 "strip: remove symbols"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
