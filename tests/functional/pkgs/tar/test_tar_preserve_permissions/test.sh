#!/bin/bash
# Functional test: tar - tar preserve permissions
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    tarSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "tar preserve permissions"
    rlRun "mkdir testdir && echo 'data' > testdir/f7.txt && chmod 644 testdir/f7.txt" 0 "Create file with perms"
    rlRun "tar -cf archive.tar --preserve-permissions testdir" 0 "tar --preserve-permissions: archive"
    rlRun "tar -xf archive.tar" 0 "extract"
    rlRun "test -f testdir/f7.txt" 0 "tar --preserve-permissions: file restored"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
