#!/bin/bash
# Functional test: grep - Multiple-patterns---e---f
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
    rlRun "echo -e 'Hello\napple' > patterns.txt" 0 "Create patterns.txt"
    rlPhaseEnd

    rlPhaseStartTest "Multiple-patterns---e---f"
    rlRun "grep -e Hello -e apple test1.txt test2.txt" 0 "Multiple patterns with -e"
    rlRun "grep -f patterns.txt test1.txt test2.txt" 0 "Patterns from file with -f"
    rlRun "test $(grep -m1 Hello test1.txt | wc -l) -eq 1" 0 "Max count: stop after first match"
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
