#!/bin/bash
# Functional test: tar - tar --strip-components
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar --strip-components"
    rlRun "mkdir -p a/b/c && echo 'deep' > a/b/c/deep.txt" 0 "Create nested dirs"
    rlRun "tar -cf archive.tar a/b/c/deep.txt" 0 "create archive"
    rlRun "tar -xf archive.tar --strip-components=3" 0 "tar --strip-components=3: strip 3 levels"
    rlRun "test -f deep.txt" 0 "tar --strip-components: file extracted"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
