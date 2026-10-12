#!/bin/bash
# Functional test: bzip2 - bzegrep command
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "bzegrep - search compressed bzip2 file"
        echo "test bzegrep line 1" > test_bzegrep.log
        echo "another line here" >> test_bzegrep.log
        echo "test bzegrep line 3" >> test_bzegrep.log
        rlRun "bzip2 test_bzegrep.log" 0 "Compress log file"
        rlRun "test -f test_bzegrep.log.bz2" 0 "Compressed file exists"
    rlPhaseEnd

    rlPhaseStartTest "bzegrep - basic pattern search"
        rlRun "bzegrep 'test bzegrep' test_bzegrep.log.bz2" 0 "bzegrep basic search works"
    rlPhaseEnd

    rlPhaseStartTest "bzegrep -c - count matches"
        rlRun "bzegrep -c 'test' test_bzegrep.log.bz2 | grep -q '2'" 0 "bzegrep -c count matches"
    rlPhaseEnd

    rlPhaseStartTest "bzegrep -n - line number display"
        rlRun "bzegrep -n 'test' test_bzegrep.log.bz2 | grep -q '1:'" 0 "bzegrep -n shows line numbers"
    rlPhaseEnd

    rlPhaseStartTest "bzegrep -v - invert match"
        rlRun "bzegrep -v 'notexist' test_bzegrep.log.bz2 | grep -q 'test'" 0 "bzegrep -v invert match works"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd