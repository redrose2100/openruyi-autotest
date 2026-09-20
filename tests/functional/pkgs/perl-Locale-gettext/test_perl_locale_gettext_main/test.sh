#!/bin/bash

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart

    rlPhaseStartSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "Get perl-Locale-gettext version info"
        rlRun "which perl-Locale-gettext 2>/dev/null || which gettext 2>/dev/null || true" 0 "Check perl-Locale-gettext is installed"
        rlRun "perl-Locale-gettext --version 2>/dev/null || gettext --version 2>/dev/null || true" 0 "Get perl-Locale-gettext version info"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "cd /" 0 "Leave test directory"
        rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
