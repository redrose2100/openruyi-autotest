#!/bin/bash

# Functional test: rpmbuild - Create-simple-spec-file

# Beakerlib-based test with lifecycle management

# Shared suite setup/cleanup via../lib.sh (install once, uninstall once)



. /usr/share/beakerlib/beakerlib.sh || exit 1

. "$(dirname "$0")/../lib.sh"



rlJournalStart

    rlPhaseStartSetup "Environment setup"

    rpmbuildSetup

    TmpDir=$(mktemp -d)

    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd



    rlPhaseStartTest "Create-simple-spec-file"

    rlRun "echo 'Name: testpkg' > $TmpDir/test.spec" 0 "create spec fileheader"

    rlRun "echo 'Version: 1.0' >> $TmpDir/test.spec" 0 "addversion"

    rlRun "echo 'Release: 1' >> $TmpDir/test.spec" 0 "add Release"

    rlRun "echo 'Summary: Test package' >> $TmpDir/test.spec" 0 "add Summary"

    rlRun "echo 'License: MIT' >> $TmpDir/test.spec" 0 "add License"

    rlRun "echo '%description' >> $TmpDir/test.spec" 0 "add %description"

    rlRun "echo 'Test package for rpmbuild' >> $TmpDir/test.spec" 0 "content"

    rlPhaseEnd





    rlPhaseStartCleanup "Clean up test environment"

    rlRun "cd /" 0 "Leave test directory"

    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then

    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"

    fi

    # rpmbuild Package managed by lib.sh's reference counting auto-uninstall

    rlPhaseEnd



    rlJournalPrintText

rlJournalEnd

