#!/bin/bash
# Functional test: attr - attr command basic operations (-s, -g, -l, -r)

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch test" 0 "Create test file"
        rlRun "ln -s test test.lnk" 0 "Create symlink"
    rlPhaseEnd

    rlPhaseStartTest "attr -s (set) and -g (get)"
        rlRun "attr -s 'oe' -V 'top' test | grep top" 0 "Set attribute via attr -s"
        rlRun "attr -g 'oe' test | grep top" 0 "Get attribute via attr -g"
    rlPhaseEnd

    rlPhaseStartTest "attr -l (list)"
        rlRun "attr -l test | grep oe" 0 "List attributes via attr -l"
    rlPhaseEnd

    rlPhaseStartTest "attr -r (remove)"
        rlRun "attr -r oe test" 0 "Remove attribute via attr -r"
        rlRun "attr -l test | grep -c oe | grep -q 0" 0 "Attribute removed"
    rlPhaseEnd

    rlPhaseStartTest "attr via symlink (-L)"
        rlRun "attr -Lq -s 'oe' -V 'top' test.lnk" 0 "Set attr via symlink with -L"
        rlRun "attr -g 'oe' test | grep top" 0 "Attribute set on target via -L"
        rlRun "attr -r oe test" 0 "Clean up attribute"
    rlPhaseEnd

    rlPhaseStartTest "attr special characters in value"
        special_value="special@chars#\$%^&123"
        rlRun "attr -s 'special' -V '$special_value' test" 0 "Set attr with special chars"
        retrieved_value=$(attr -g 'special' test 2>&1 | tail -1)
        if [ "$retrieved_value" = "$special_value" ]; then
            rlPass "Special characters preserved correctly"
        else
            rlFail "Special characters not preserved: got '$retrieved_value', expected '$special_value'"
        fi
        rlRun "attr -r 'special' test" 0 "Clean up special attribute"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd