#!/bin/bash
# Functional test: gdbm - gdbmtool database operations
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y gdbm 2>/dev/null
    rlPhaseEnd

    rlPhaseStartTest "gdbmtool help"
        rlRun "gdbmtool --help 2>&1 | grep -qiE 'Usage|usage'" 0 "gdbmtool displays help"
    rlPhaseEnd

    rlPhaseStartTest "gdbmtool create new database"
        gdbmtool -n "$TmpDir/test.gdbm" > "$TmpDir/create.log" << 'EOF'
list
status
quit
EOF
        rlRun "test -f $TmpDir/test.gdbm" 0 "gdbmtool creates database file"
    rlPhaseEnd

    rlPhaseStartTest "gdbmtool open/close/status"
        gdbmtool > "$TmpDir/controls.log" << GDBM_EOF
status
open $TmpDir/test.gdbm
status
close
status
quit
GDBM_EOF
        count=$(grep -c "Database is not open" "$TmpDir/controls.log")
        rlRun "test \"$count\" = '2'" 0 "gdbmtool open/close: expected 2 'not open' messages"
        rlRun "grep -q 'Database is open' $TmpDir/controls.log" 0 "gdbmtool confirms open state"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd