#!/bin/bash
# Functional test: elfutils - version and help
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    elfutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlPhaseEnd

    rlPhaseStartTest "version and help"
    rlRun "eu-addr2line --version 2>&1 " 0 "eu-addr2line version info"
    rlRun "eu-addr2line --help 2>&1 | head -5 || true" 0 "eu-addr2line help info"
    rlRun "eu-ar --version 2>&1 " 0 "eu-ar version info"
    rlRun "eu-ar --help 2>&1 | head -5 || true" 0 "eu-ar help info"
    rlRun "eu-elfclassify --version 2>&1 " 0 "eu-elfclassify version info"
    rlRun "eu-elfclassify --help 2>&1 | head -5 || true" 0 "eu-elfclassify help info"
    rlRun "eu-elfcmp --version 2>&1 " 0 "eu-elfcmp version info"
    rlRun "eu-elfcmp --help 2>&1 | head -5 || true" 0 "eu-elfcmp help info"
    rlRun "eu-elfcompress --version 2>&1 " 0 "eu-elfcompress version info"
    rlRun "eu-elfcompress --help 2>&1 | head -5 || true" 0 "eu-elfcompress help info"
    rlRun "eu-elflint --version 2>&1 " 0 "eu-elflint version info"
    rlRun "eu-elflint --help 2>&1 | head -5 || true" 0 "eu-elflint help info"
    rlRun "eu-findtextrel --version 2>&1 " 0 "eu-findtextrel version info"
    rlRun "eu-findtextrel --help 2>&1 | head -5 || true" 0 "eu-findtextrel help info"
    rlRun "eu-make-debug-archive --version 2>&1 " 0 "eu-make-debug-archive version info"
    rlRun "eu-make-debug-archive --help 2>&1 | head -5 || true" 0 "eu-make-debug-archive help info"
    rlRun "eu-nm --version 2>&1 " 0 "eu-nm version info"
    rlRun "eu-nm --help 2>&1 | head -5 || true" 0 "eu-nm help info"
    rlRun "eu-objdump --version 2>&1 " 0 "eu-objdump version info"
    rlRun "eu-objdump --help 2>&1 | head -5 || true" 0 "eu-objdump help info"
    rlRun "eu-ranlib --version 2>&1 " 0 "eu-ranlib version info"
    rlRun "eu-ranlib --help 2>&1 | head -5 || true" 0 "eu-ranlib help info"
    rlRun "eu-readelf --version 2>&1 " 0 "eu-readelf version info"
    rlRun "eu-readelf --help 2>&1 | head -5 || true" 0 "eu-readelf help info"
    rlRun "eu-size --version 2>&1 " 0 "eu-size version info"
    rlRun "eu-size --help 2>&1 | head -5 || true" 0 "eu-size help info"
    rlRun "eu-srcfiles --version 2>&1 " 0 "eu-srcfiles version info"
    rlRun "eu-srcfiles --help 2>&1 | head -5 || true" 0 "eu-srcfiles help info"
    rlRun "eu-stack --version 2>&1 " 0 "eu-stack version info"
    rlRun "eu-stack --help 2>&1 | head -5 || true" 0 "eu-stack help info"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # elfutils Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
