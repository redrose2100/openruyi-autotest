#!/bin/bash
# Functional test: tar - tar --delete from archive
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar --delete from archive"
    rlRun "mkdir testdir && echo 'a' > testdir/a.txt && echo 'b' > testdir/b.txt" 0 "Create test data"
    rlRun "tar -cf archive.tar testdir" 0 "create archive"
    rlRun "tar --delete -f archive.tar testdir/a.txt" 0 "tar --delete: remove file"
    rlRun "tar -tf archive.tar | grep -v 'a.txt'" 0 "tar --delete: a.txt removed"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
