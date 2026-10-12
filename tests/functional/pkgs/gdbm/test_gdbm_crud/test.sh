#!/bin/bash
# Functional test: gdbm - gdbmtool CRUD operations
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y gdbm 2>/dev/null
    rlPhaseEnd

    rlPhaseStartTest "gdbmtool default config display"
        gdbmtool -n "$TmpDir/test.gdbm" > "$TmpDir/config.log" << 'EOF'
list
set
quit
EOF
        rlRun "grep -q 'blocksize is unset' $TmpDir/config.log" 0 "gdbmtool displays default blocksize config"
    rlPhaseEnd

    rlPhaseStartTest "gdbmtool store and fetch"
        gdbmtool "$TmpDir/test.gdbm" > "$TmpDir/store.log" << 'EOF'
store test_key get_value_success
quit
EOF
        gdbmtool "$TmpDir/test.gdbm" > "$TmpDir/fetch.log" << 'EOF'
fetch test_key
quit
EOF
        rlRun "grep -q 'get_value_success' $TmpDir/fetch.log" 0 "gdbmtool fetch returns stored value"
    rlPhaseEnd

    rlPhaseStartTest "gdbmtool delete"
        gdbmtool "$TmpDir/test.gdbm" > "$TmpDir/delete.log" 2>&1 << 'EOF'
delete test_key
fetch test_key
quit
EOF
        rlRun "grep -q 'get_value_success' $TmpDir/delete.log; test \$? -ne 0" 0 "gdbmtool delete removes key"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd