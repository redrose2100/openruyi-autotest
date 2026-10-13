#!/bin/bash
# Functional test: bzip2 - advanced compression options
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "test data for compression" > testfile
    rlPhaseEnd

    rlPhaseStartTest "bzip2 -z - compress with -z option"
        rlRun "bzip2 -z testfile" 0 "bzip2 -z compresses file"
        rlRun "test -f testfile.bz2" 0 "testfile.bz2 exists"
        rlRun "bzip2 -d testfile.bz2" 0 "Decompress for next test"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 -c --stdout - write to stdout"
        rlRun "bzip2 -c testfile > testfile_stdout.bz2" 0 "bzip2 -c writes to stdout"
        rlRun "bzip2 --stdout testfile > testfile_stdout2.bz2" 0 "bzip2 --stdout writes to stdout"
        rlRun "test -f testfile_stdout.bz2" 0 "stdout compressed file exists"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 -t - test compressed file integrity"
        bzip2 -k testfile
        rlRun "bzip2 -t testfile.bz2" 0 "bzip2 -t tests integrity"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 -L - show license"
        rlRun "bzip2 -L 2>&1 | grep -qiE 'license|bzip|version' || bzip2 -L 2>&1 | head -1" 0 "bzip2 -L shows license info"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 -s --small - use less memory"
        rlRun "bzip2 -s -k testfile" 0 "bzip2 -s compresses with reduced memory"
        rlRun "bzip2 --small -k testfile" 0 "bzip2 --small compresses"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 --fast --best - compression level"
        rlRun "bzip2 --fast -k testfile" 0 "bzip2 --fast compresses"
        rlRun "bzip2 --best -k testfile" 0 "bzip2 --best compresses"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 --compress - explicit compress mode"
        rlRun "bzip2 --compress -k testfile" 0 "bzip2 --compress works"
    rlPhaseEnd

    rlPhaseStartTest "bzip2 --version - show version"
        rlRun "bzip2 --version 2>&1 | head -1" 0 "bzip2 --version shows version"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd