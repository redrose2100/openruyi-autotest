#!/bin/bash
# Functional test: wget - wget --save-cookies
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    wgetSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"

    rlPhaseEnd

    rlPhaseStartTest "wget --save-cookies"
    rlRun "wget --save-cookies cookie.txt --keep-session-cookies http://example.com -q -O /dev/null" 0 "wget --save-cookies: save cookies"
    rlRun "test -f cookie.txt" 0 "wget --save-cookies: cookie file created"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
