#!/bin/bash
# Functional test: systemd - journalctl---Journal-query
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    systemdSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "journalctl---Journal-query"
    rlRun "journalctl --version" 0 "journalctl version"
    rlRun "journalctl -n 5 2>&1 " 0 "journalctl -n: last entries"
    rlRun "journalctl -b 2>&1 | head -5" 0 "journalctl -b: current boot"
    rlRun "journalctl --list-boots 2>&1 | head -5" 0 "journalctl --list-boots"
    rlRun "journalctl -k 2>&1 | head -5" 0 "journalctl -k: kernel messages"
    rlRun "journalctl --no-pager -n 3 -o short 2>&1 " 0 "journalctl -o short: short format"
    rlRun "journalctl --no-pager -n 3 -o json 2>&1 | head -5" 0 "journalctl -o json: json format"
    rlRun "journalctl --no-pager -n 3 -o verbose 2>&1 | head -5" 0 "journalctl -o verbose"
    rlRun "journalctl --disk-usage 2>&1 " 0 "journalctl --disk-usage"
    rlRun "journalctl --no-pager -n 1 --output=cat 2>&1 " 0 "journalctl --output=cat"
    rlRun "journalctl --no-pager -n 2 -p err 2>&1 " 0 "journalctl -p err: error messages"
    rlRun "journalctl --no-pager --since \"1 hour ago\" 2>&1 | head -3" 0 "journalctl --since"
    rlRun "journalctl --no-pager -n 1 -q 2>&1 " 0 "journalctl -q: quiet"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # systemd Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
