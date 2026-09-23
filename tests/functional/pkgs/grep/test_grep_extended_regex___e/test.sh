#!/bin/bash
# Functional test: grep - Extended-regex---E
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
    rlRun "echo -e 'apple pie\nbanana split\napple juice\norange juice' > test2.txt" 0 "Create test2.txt"
    rlPhaseEnd

    rlPhaseStartTest "Extended-regex---E"
    rlRun "grep -E \"apple|banana\" test2.txt" 0 "Extended regex with alternation"
    rlRun "grep -E \"[0-9]+\" test1.txt" 0 "Extended regex: digit quantifier"
    rlRun "test $(grep -E \"[0-9]+\" test1.txt | wc -l) -ge 1" 0 "Verify digit match count"
    rlRun "egrep \"apple|banana\" test2.txt" 0 "egrep equivalent to grep -E"
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
