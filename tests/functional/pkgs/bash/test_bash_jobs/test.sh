#!/bin/bash
# Functional test: bash - jobs builtin
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "jobs - List no jobs when none are running"
        rlRun "jobs" 0 "jobs executes successfully"
        rlRun "test -z \"\$(jobs)\"" 0 "No jobs listed when none are active"
    rlPhaseEnd

    rlPhaseStartTest "jobs - List background jobs"
        sleep 30 &
        bg_pid=$!
        rlRun "sleep 30 &" 0 "Start background process"
        rlRun "jobs | grep -c 'sleep' | grep -E '[12]'" 0 "jobs shows background sleep processes"
    rlPhaseEnd

    rlPhaseStartTest "jobs -l - List jobs with PIDs"
        rlRun "jobs -l" 0 "jobs -l executes successfully"
        rlRun "jobs -l | grep -E '[0-9]+'" 0 "jobs -l shows process IDs"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        # Kill any remaining background jobs from this test
        rlRun "kill %1 %2 2>/dev/null; true" 0 "Kill background jobs"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd