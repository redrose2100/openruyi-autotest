#!/bin/bash
# Functional test: acl - getfacl extra options (-s, -R, -L, -P)

. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        uid=$(whoami)
        touch file
        ln -s file filelink
        mkdir -p dir/subdir
        rlRun "setfacl -d -m user:${uid}:rwx dir" 0 "Set default ACL on dir"
    rlPhaseEnd

    rlPhaseStartTest "getfacl -s (skip base)"
        rlRun "getfacl -s file dir > result" 0 "Run getfacl -s"
        rlRun "! grep -q '# file: file' result" 0 "File with only base entries omitted by -s"
    rlPhaseEnd

    rlPhaseStartTest "getfacl -R (recursive)"
        rlRun "getfacl -R dir > result" 0 "Run getfacl -R"
        rlRun "grep -q '# file: dir/subdir' result" 0 "Subdirectory included by -R"
    rlPhaseEnd

    rlPhaseStartTest "getfacl -L (follow symlinks)"
        rlRun "getfacl -L filelink > result" 0 "Run getfacl -L"
        rlRun "grep -q '# file: filelink' result" 0 "Symlink followed by -L"
    rlPhaseEnd

    rlPhaseStartTest "getfacl -P (physical, no follow)"
        rlRun "getfacl -P filelink > result" 0 "Run getfacl -P"
        rlRun "grep -q '# file: file' result" 0 "Symlink target shown by -P"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd