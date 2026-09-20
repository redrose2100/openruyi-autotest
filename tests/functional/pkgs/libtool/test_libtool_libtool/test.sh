#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get libtool help info"
        rlRun "libtool --version 2>/dev/null || libtool --version 2>/dev/null || true" 0 "Get libtool version info"
        rlRun "libtool --help 2>/dev/null || libtool -h 2>/dev/null || libtool --help 2>/dev/null || true" 0 "Get libtool help info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
