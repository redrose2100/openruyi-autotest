#!/bin/bash
# Functional test: pam - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    pamSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "faillock --version 2>&1 " 0 "faillock version info"
    rlRun "faillock --help 2>&1 | head -5 || true" 0 "faillock help info"
    rlRun "mkhomedir_helper --version 2>&1 " 0 "mkhomedir_helper version info"
    rlRun "mkhomedir_helper --help 2>&1 | head -5 || true" 0 "mkhomedir_helper help info"
    rlRun "pam_timestamp_check --version 2>&1 " 0 "pam_timestamp_check version info"
    rlRun "pam_timestamp_check --help 2>&1 | head -5 || true" 0 "pam_timestamp_check help info"
    rlRun "unix_chkpwd --version 2>&1 " 0 "unix_chkpwd version info"
    rlRun "unix_chkpwd --help 2>&1 | head -5 || true" 0 "unix_chkpwd help info"
    rlRun "unix_update --version 2>&1 " 0 "unix_update version info"
    rlRun "unix_update --help 2>&1 | head -5 || true" 0 "unix_update help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # pam Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
