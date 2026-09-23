#!/bin/bash
# Functional test: grep - Fixed-strings---F
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    grepSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo -e 'Hello World\nHello Linux\nThis is a test\nHello everyone\nLine with numbers 123\nSpecial chars: *.[]^$\nWorld is here' > test1.txt" 0 "Create test1.txt"
    rlPhaseEnd

    rlPhaseStartTest "Fixed-strings---F"
    rlRun "grep -F \"Special chars: *.[]^$\" test1.txt" 0 "Fixed string with special chars"
    rlRun "grep -F \"*.[]\" test1.txt" 0 "Fixed string: no regex meta-char interpretation"
    rlRun "fgrep \"Special chars\" test1.txt" 0 "fgrep equivalent to grep -F"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # grep Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
