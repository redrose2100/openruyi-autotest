#!/bin/bash
# Functional test: coreutils - paste merge lines
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"


    rlPhaseEnd

    rlPhaseStartTest "paste merge lines"
    rlRun "echo -e 'a\nb' > paste1.txt" 0 "Create paste file 1"
    rlRun "echo -e '1\n2' > paste2.txt" 0 "Create paste file 2"
    rlRun "paste paste1.txt paste2.txt" 0 "paste merge files"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
