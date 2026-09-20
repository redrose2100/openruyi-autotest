#!/usr/bin/env python3
"""Split acl multi-checkpoint test files into individual checkpoint test cases.

Each new test file:
- Self-contained setup (tmpdir + test files) and cleanup
- One checkpoint per file
- No dependency on lib.sh (package managed by tmt require in main.fmf)
"""

import os, shutil, textwrap, inspect, stat, subprocess

BASE = r"e:\code\openruyi-autotest"
ACL = os.path.join(BASE, "tests", "functional", "pkgs", "acl")

HEADER = """#!/bin/bash
# Functional test: acl - {desc_en}
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
{setup_extra}
    rlPhaseEnd

    rlPhaseStartTest "{desc_zh}"
{test_body}
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
"""

FMF = """summary: Functional test - acl - {desc_en}
test: ./test.sh
tag:
 - functional
 - acl
duration: 1m
tier: 1
path: /tests/functional/pkgs/acl/{dirname}
require:
 - acl
 - beakerlib
"""

# ============================================================
# Checkpoint definitions: (dirname, desc_en, desc_zh, setup_extra, test_body)
# ============================================================

CHECKPOINTS = [

    # ===== test_acl_getfacl_basic =====
    (
        "test_acl_getfacl_view_file_default_acl",
        "getfacl - view file default ACL",
        "view file default ACL",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "getfacl testfile > out.txt 2>&1" 0 "getfacl testfile"
        rlAssertGrep "user::" out.txt
        rlAssertGrep "group::" out.txt
        rlAssertGrep "other::" out.txt""",
    ),
    (
        "test_acl_getfacl_view_dir_default_acl",
        "getfacl - view directory default ACL",
        "view directory default ACL",
        """rlRun "mkdir testdir" 0 "Create test directory" """,
        """rlRun "getfacl testdir > out.txt 2>&1" 0 "getfacl testdir"
        rlAssertGrep "user::" out.txt
        rlAssertGrep "group::" out.txt""",
    ),
    (
        "test_acl_getfacl_param_a_access_acl",
        "getfacl -a show access ACL only",
        "use -a to show access ACL only",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "getfacl -a testfile > out.txt 2>&1" 0 "getfacl -a"
        rlAssertGrep "user::" out.txt
        if getfacl -a testfile 2>&1 | grep -q "default:"; then
            rlFail "-a output contains default entries"
        else
            rlPass "-a output contains no default entries"
        fi""",
    ),
    (
        "test_acl_getfacl_view_default_acl_entries",
        "getfacl - view default ACL entries on directory",
        "view default ACL entries on directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u::rwx,d:g::r-x,d:o::--- testdir" 0 "set default ACL"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "getfacl testdir"
        rlAssertGrep "default:user::rwx" out.txt
        rlAssertGrep "default:group::r-x" out.txt
        rlAssertGrep "default:other::---" out.txt""",
    ),
    (
        "test_acl_getfacl_param_c_no_header",
        "getfacl -c suppress header comment",
        "use -c to suppress header comment",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "getfacl -c testfile > out.txt 2>&1" 0 "getfacl -c"
        rlAssertNotGrep "^# file:" out.txt""",
    ),
    (
        "test_acl_getfacl_param_n_numeric",
        "getfacl -n display numeric UID/GID",
        "use -n to display numeric IDs",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "getfacl -n testfile > out.txt 2>&1" 0 "getfacl -n"
        rlAssertGrep "[0-9]" out.txt""",
    ),
    (
        "test_acl_getfacl_param_t_tabular",
        "getfacl -t tabular output format",
        "use -t for tabular output",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "getfacl -t testfile > out.txt 2>&1" 0 "getfacl -t"
        rlAssertGrep "[r-][w-][x-]" out.txt""",
    ),

    # ===== test_acl_setfacl_basic =====
    (
        "test_acl_setfacl_modify_user_rwx",
        "setfacl -m set user rwx permission",
        "set user root rwx permission",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx testfile" 0 "set user root rwx"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify ACL"
        rlAssertGrep "user:root:rwx" out.txt""",
    ),
    (
        "test_acl_setfacl_modify_group_rx",
        "setfacl -m set group r-x permission",
        "set group root r-x permission",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m g:root:r-x testfile" 0 "set group root r-x"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify ACL"
        rlAssertGrep "group:root:r-x" out.txt""",
    ),
    (
        "test_acl_setfacl_modify_other_readonly",
        "setfacl -m set other readonly",
        "set other readonly permission",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m o::r-- testfile" 0 "set other readonly"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify ACL"
        rlAssertGrep "other::r--" out.txt""",
    ),
    (
        "test_acl_setfacl_modify_mask_rwx",
        "setfacl -m set mask to rwx",
        "set mask to rwx",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m m::rwx testfile" 0 "set mask rwx"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify mask"
        rlAssertGrep "mask::rwx" out.txt""",
    ),
    (
        "test_acl_setfacl_param_n_no_recalc_mask",
        "setfacl -n do not recalculate mask",
        "use -n to not recalculate mask",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -n -m u:root:r-- testfile" 0 "setfacl -n"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify ACL" """,
    ),

    # ===== test_acl_setfacl_advanced =====
    (
        "test_acl_setfacl_default_user_acl",
        "setfacl - set default user ACL on directory",
        "set default user ACL on directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx testdir" 0 "set default user ACL"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "verify"
        rlAssertGrep "default:user:root:rwx" out.txt""",
    ),
    (
        "test_acl_setfacl_default_group_acl",
        "setfacl - set default group ACL on directory",
        "set default group ACL on directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:g:root:r-x testdir" 0 "set default group ACL"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "verify" """,
    ),
    (
        "test_acl_setfacl_default_mask",
        "setfacl - set default mask on directory",
        "set default mask on directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:m::rwx testdir" 0 "set default mask"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "verify" """,
    ),
    (
        "test_acl_setfacl_default_other",
        "setfacl - set default other on directory",
        "set default other on directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:o::r-- testdir" 0 "set default other"
        rlRun "getfacl testdir > out.txt 2>&1" 0 "verify" """,
    ),
    (
        "test_acl_setfacl_set_replace_acl",
        "setfacl --set replace entire ACL",
        "use --set to replace entire ACL",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl --set u::rw-,u:root:rwx,g::r--,o::r--,m::rwx testfile" 0 "setfacl --set"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify"
        rlAssertGrep "user:root:rwx" out.txt""",
    ),
    (
        "test_acl_setfacl_restore_from_rules_file",
        "setfacl -M apply ACL from file",
        "apply ACL from rules file",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "echo 'u:root:rw-' > acl_rules.txt" 0 "create rules file"
        rlRun "setfacl -M acl_rules.txt testfile" 0 "apply from file"
        rlRun "getfacl testfile > out.txt 2>&1" 0 "verify" """,
    ),

    # ===== test_acl_setfacl_remove =====
    (
        "test_acl_setfacl_remove_user_entry",
        "setfacl -x remove user ACL entry",
        "remove user root ACL entry",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx testfile" 0 "pre-set user ACL"
        rlRun "setfacl -x u:root testfile" 0 "remove user entry"
        output=$(getfacl testfile 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'user:root:'" 0 "confirm removed" """,
    ),
    (
        "test_acl_setfacl_remove_group_entry",
        "setfacl -x remove group ACL entry",
        "remove group root ACL entry",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m g:root:r-x testfile" 0 "pre-set group ACL"
        rlRun "setfacl -x g:root testfile" 0 "remove group entry"
        output=$(getfacl testfile 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'group:root:'" 0 "confirm removed" """,
    ),
    (
        "test_acl_setfacl_remove_all_acl",
        "setfacl -b remove all extended ACL",
        "remove all extended ACL entries",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "pre-set ACL"
        rlRun "setfacl -b testfile" 0 "remove all ACL"
        output=$(getfacl testfile 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'user:root:'" 0 "confirm no extended ACL" """,
    ),
    (
        "test_acl_setfacl_remove_default_acl",
        "setfacl -k remove default ACL from directory",
        "remove default ACL from directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx testdir" 0 "pre-set default ACL"
        rlRun "setfacl -k testdir" 0 "remove default ACL"
        output=$(getfacl testdir 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'default:'" 0 "confirm no default ACL" """,
    ),
    (
        "test_acl_setfacl_remove_from_rules_file",
        "setfacl -X remove ACL by rule file",
        "remove ACL by rule file",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "echo 'u:root' > remove_rules.txt" 0 "create remove rules"
        rlRun "setfacl -m u:root:rwx testfile" 0 "pre-set ACL"
        rlRun "setfacl -X remove_rules.txt testfile" 0 "remove by file"
        output=$(getfacl testfile 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'user:root:'" 0 "confirm removed" """,
    ),

    # ===== test_acl_setfacl_recursive =====
    (
        "test_acl_setfacl_recursive_set",
        "setfacl -R recursively set ACL",
        "recursively set ACL on sub-files",
        """rlRun "mkdir -p testdir/subdir1/subdir2" 0 "create nested dirs"
        rlRun "touch testdir/file1 testdir/subdir1/file2" 0 "create test files" """,
        """rlRun "setfacl -R -m u:root:rw- testdir" 0 "recursive set ACL"
        output1=$(getfacl testdir/file1 2>&1)
        output2=$(getfacl testdir/subdir1/file2 2>&1)
        rlRun "echo \\"\\$output1\\" | grep -q 'user:root:rw-'" 0 "verify file1"
        rlRun "echo \\"\\$output2\\" | grep -q 'user:root:rw-'" 0 "verify subdir1/file2" """,
    ),
    (
        "test_acl_setfacl_recursive_remove",
        "setfacl -R -b recursively remove ACL",
        "recursively remove ACL from all files",
        """rlRun "mkdir -p testdir/subdir1" 0 "create nested dirs"
        rlRun "touch testdir/file1 testdir/subdir1/file2" 0 "create test files"
        rlRun "setfacl -R -m u:root:rw- testdir" 0 "pre-set ACL" """,
        """rlRun "setfacl -R -b testdir" 0 "recursive remove ACL"
        output1=$(getfacl testdir/file1 2>&1)
        output2=$(getfacl testdir/subdir1/file2 2>&1)
        rlRun "! echo \\"\\$output1\\" | grep -q 'user:root:'" 0 "verify file1 cleared"
        rlRun "! echo \\"\\$output2\\" | grep -q 'user:root:'" 0 "verify subdir1/file2 cleared" """,
    ),

    # ===== test_acl_setfacl_backup_restore =====
    (
        "test_acl_getfacl_backup_file_acl",
        "getfacl backup - save file ACL to backup",
        "back up file ACL",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "set ACL"
        rlRun "getfacl testfile > acl.backup" 0 "getfacl backup"
        rlRun "test -f acl.backup" 0 "backup file created"
        rlRun "grep -q '^# file:' acl.backup" 0 "backup has file header" """,
    ),
    (
        "test_acl_setfacl_restore_file_acl",
        "setfacl --restore file ACL from backup",
        "restore file ACL from backup",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx,g:root:r-x testfile" 0 "set ACL"
        rlRun "getfacl testfile > acl.backup" 0 "create backup"
        rlRun "setfacl -b testfile" 0 "clear ACL"
        rlRun "setfacl --restore=acl.backup" 0 "restore from backup"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "user entry restored"
        rlRun "echo \\"\\$output\\" | grep -q 'group:root:r-x'" 0 "group entry restored" """,
    ),
    (
        "test_acl_getfacl_backup_dir_default_acl",
        "getfacl backup - save directory default ACL",
        "back up directory default ACL entries",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x testdir" 0 "set default ACL"
        rlRun "getfacl testdir 2>&1 | grep 'default:' > out.txt" 0 "get default entries"
        rlAssertGrep "default:user:root:rwx" out.txt
        rlAssertGrep "default:group:root:r-x" out.txt""",
    ),
    (
        "test_acl_setfacl_restore_dir_acl",
        "setfacl --restore directory ACL from backup",
        "restore directory ACL from backup",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x testdir" 0 "set default ACL"
        rlRun "getfacl testdir > dir.backup" 0 "create dir backup"
        rlRun "setfacl -k testdir" 0 "clear default ACL"
        rlRun "cd $TmpDir && setfacl --restore=dir.backup" 0 "restore dir from backup"
        output=$(getfacl testdir 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:root:rwx'" 0 "default user restored"
        rlRun "echo \\"\\$output\\" | grep -q 'default:group:root:r-x'" 0 "default group restored" """,
    ),

    # ===== test_acl_setfacl_symlink =====
    (
        "test_acl_setfacl_symlink_follow",
        "setfacl -L follow symlink to set ACL",
        "use -L to follow symlink",
        """rlRun "touch testfile" 0 "Create test file"
        rlRun "ln -s testfile symlink" 0 "create symlink" """,
        """rlRun "setfacl -L -m u:root:rwx symlink" 0 "setfacl -L"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "symlink target has ACL" """,
    ),
    (
        "test_acl_setfacl_symlink_nofollow",
        "setfacl -P do not follow symlink",
        "use -P to not follow symlink",
        """rlRun "touch testfile" 0 "Create test file"
        rlRun "ln -s testfile symlink" 0 "create symlink" """,
        """rlRun "setfacl -P -m u:root:r-- symlink" 0 "setfacl -P on symlink" """,
    ),

    # ===== test_acl_acl_inheritance =====
    (
        "test_acl_inheritance_file_inherits_default",
        "ACL inheritance - new file inherits default ACL",
        "new file inherits default ACL",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x,d:o::r-- testdir" 0 "set default ACL"
        rlRun "touch testdir/newfile" 0 "create new file"
        output=$(getfacl testdir/newfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "file inherits user default"
        rlRun "echo \\"\\$output\\" | grep -q 'group:root:r-x'" 0 "file inherits group default" """,
    ),
    (
        "test_acl_inheritance_subdir_inherits_default",
        "ACL inheritance - subdirectory inherits default ACL",
        "subdirectory inherits default ACL",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:g:root:r-x,d:o::r-- testdir" 0 "set default ACL"
        rlRun "mkdir testdir/newsubdir" 0 "create subdirectory"
        output=$(getfacl testdir/newsubdir 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:root:rwx'" 0 "subdir inherits default user"
        rlRun "echo \\"\\$output\\" | grep -q 'default:group:root:r-x'" 0 "subdir inherits default group" """,
    ),

    # ===== test_acl_acl_permission_verify =====
    (
        "test_acl_permission_set_full_acl",
        "ACL permission - set and verify full ACL entries",
        "set and verify full ACL entries",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl --set u::rwx,u:root:rwx,g::r-x,o::r--,m::rwx testfile" 0 "set full ACL"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user::rwx'" 0 "user::rwx"
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "user:root:rwx"
        rlRun "echo \\"\\$output\\" | grep -q 'group::r-x'" 0 "group::r-x"
        rlRun "echo \\"\\$output\\" | grep -q 'mask::rwx'" 0 "mask::rwx" """,
    ),
    (
        "test_acl_permission_mask_truncates",
        "ACL permission - mask truncates effective permissions",
        "mask truncates effective permissions",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx,m::r-- testfile" 0 "set mask limited"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'mask::r--'" 0 "mask::r--"
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "entry preserved"
        rlRun "getfacl -e testfile > out.txt 2>&1" 0 "show effective permissions"
        rlAssertGrep "user:root:rwx.*#effective:r--" out.txt
        rlAssertGrep "group::r--.*#effective:r--" out.txt""",
    ),
    (
        "test_acl_permission_mask_restore",
        "ACL permission - raise mask restores effective permissions",
        "raise mask to restore effective permissions",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx testfile" 0 "set user ACL"
        rlRun "setfacl -m m::rwx testfile" 0 "raise mask to rwx"
        rlRun "getfacl -e testfile > out.txt 2>&1" 0 "show effective permissions"
        rlAssertGrep "user:root:rwx.*#effective:rwx" out.txt""",
    ),

    # ===== test_acl_chacl_command =====
    (
        "test_acl_setfacl_set_named_user_acl",
        "setfacl - set named user ACL entry",
        "set named user ACL entry",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx,g::r--,o::r-- testfile" 0 "set ACL"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "named user ACL set" """,
    ),
    (
        "test_acl_setfacl_recursive_apply_to_subfile",
        "setfacl -R apply ACL recursively to sub-files",
        "recursively apply ACL to sub-files",
        """rlRun "mkdir -p testdir" 0 "Create test directory"
        rlRun "touch testdir/file1" 0 "create sub-file" """,
        """rlRun "setfacl -R -m u:root:rwx,g::r--,o::r-- testdir" 0 "recursive setfacl"
        output=$(getfacl testdir/file1 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "sub-file has ACL" """,
    ),
    (
        "test_acl_setfacl_default_and_access_coexist",
        "setfacl - default and access ACL coexist on directory",
        "default and access ACL coexist on directory",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:g::r-x,d:o::r-x testdir" 0 "set default ACL"
        rlRun "setfacl -m u:root:rwx,g::r-x,o::r-x testdir" 0 "set access ACL"
        output=$(getfacl testdir 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:root:rwx'" 0 "default ACL present"
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "access ACL present" """,
    ),

    # ===== test_acl_default_named_entries =====
    (
        "test_acl_default_named_user_and_group",
        "default ACL - set named user and group entries",
        "set named user and group default ACL entries",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x,d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named entries"
        output=$(getfacl testdir 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:root:rwx'" 0 "default user root"
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:daemon:r-x'" 0 "default user daemon"
        rlRun "echo \\"\\$output\\" | grep -q 'default:group:root:r-x'" 0 "default group root"
        rlRun "echo \\"\\$output\\" | grep -q 'default:group:wheel:r--'" 0 "default group wheel" """,
    ),
    (
        "test_acl_default_file_inherits_named_entries",
        "default ACL - new file inherits named entries",
        "new file inherits named default ACL entries",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x,d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named entries"
        rlRun "touch testdir/newfile" 0 "create new file"
        output=$(getfacl testdir/newfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "file inherits user root"
        rlRun "echo \\"\\$output\\" | grep -q 'user:daemon:r-x'" 0 "file inherits user daemon"
        rlRun "echo \\"\\$output\\" | grep -q 'group:root:r-x'" 0 "file inherits group root"
        rlRun "echo \\"\\$output\\" | grep -q 'group:wheel:r--'" 0 "file inherits group wheel" """,
    ),
    (
        "test_acl_default_subdir_inherits_named_entries",
        "default ACL - subdirectory inherits named default entries",
        "subdirectory inherits named default ACL entries",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x,d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named entries"
        rlRun "mkdir testdir/newsubdir" 0 "create subdirectory"
        output=$(getfacl testdir/newsubdir 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:daemon:r-x'" 0 "subdir inherits default user"
        rlRun "echo \\"\\$output\\" | grep -q 'default:group:wheel:r--'" 0 "subdir inherits default group" """,
    ),
    (
        "test_acl_default_remove_named_user",
        "default ACL - remove named user from default ACL",
        "remove named user from default ACL",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:u:root:rwx,d:u:daemon:r-x testdir" 0 "set named user entries"
        rlRun "setfacl -x d:u:daemon testdir" 0 "remove daemon user"
        output=$(getfacl testdir 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'default:user:daemon:'" 0 "daemon removed"
        rlRun "echo \\"\\$output\\" | grep -q 'default:user:root:rwx'" 0 "root preserved" """,
    ),
    (
        "test_acl_default_remove_named_group",
        "default ACL - remove named group from default ACL",
        "remove named group from default ACL",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "setfacl -m d:g:root:r-x,d:g:wheel:r-- testdir" 0 "set named group entries"
        rlRun "setfacl -x d:g:wheel testdir" 0 "remove wheel group"
        output=$(getfacl testdir 2>&1)
        rlRun "! echo \\"\\$output\\" | grep -q 'default:group:wheel:'" 0 "wheel removed" """,
    ),

    # ===== test_acl_error_handling =====
    (
        "test_acl_getfacl_nonexistent_file",
        "getfacl - error on nonexistent file",
        "getfacl on nonexistent file fails",
        "",
        'rlRun "getfacl nonexistent_file" 1-255 "getfacl on nonexistent file fails"',
    ),
    (
        "test_acl_setfacl_nonexistent_file",
        "setfacl - error on nonexistent file",
        "setfacl on nonexistent file fails",
        "",
        'rlRun "setfacl -m u:root:rwx nonexistent_file" 1-255 "setfacl on nonexistent file fails"',
    ),
    (
        "test_acl_setfacl_invalid_permission",
        "setfacl - reject invalid permission string",
        "invalid permission string rejected",
        'rlRun "touch testfile" 0 "Create test file"',
        'rlRun "setfacl -m u:root:xyz testfile" 1-255 "invalid permission rejected"',
    ),
    (
        "test_acl_setfacl_invalid_acl_type",
        "setfacl - reject invalid ACL type tag",
        "invalid ACL type tag rejected",
        'rlRun "touch testfile" 0 "Create test file"',
        'rlRun "setfacl -m x:root:rw testfile" 1-255 "invalid ACL type rejected"',
    ),
    (
        "test_acl_setfacl_nonexistent_user",
        "setfacl - reject nonexistent user",
        "nonexistent user rejected",
        'rlRun "touch testfile" 0 "Create test file"',
        'rlRun "setfacl -m u:no_such_user:rwx testfile" 1-255 "nonexistent user rejected"',
    ),
    (
        "test_acl_setfacl_nonexistent_group",
        "setfacl - reject nonexistent group",
        "nonexistent group rejected",
        'rlRun "touch testfile" 0 "Create test file"',
        'rlRun "setfacl -m g:no_such_group:rwx testfile" 1-255 "nonexistent group rejected"',
    ),
    (
        "test_acl_setfacl_invalid_perm_string",
        "setfacl - reject invalid permission format",
        "invalid permission format rejected",
        'rlRun "touch testfile" 0 "Create test file"',
        'rlRun "setfacl -m u:root:zz testfile" 1-255 "invalid perm format rejected"',
    ),
    (
        "test_acl_setfacl_permission_denied",
        "setfacl - permission denied on protected file",
        "permission denied on protected file",
        'rlRun "touch testfile" 0 "Create test file"',
        """        if [ "$(id -u)" = "0" ]; then
            rlRun "sudo -n -u openruyi setfacl -m u:root:rwx /root/test 2>&1" 1-255 "non-root cannot set ACL"
        else
            rlRun "setfacl -m u:root:rwx /root/test 2>&1" 1-255 "non-root cannot set ACL"
        fi
        rlPass "Permission denied handled correctly"
        """,
    ),

    # ===== test_acl_special_cases =====
    (
        "test_acl_setfacl_multi_user_and_group",
        "setfacl - set multiple user and group ACL entries",
        "set multiple user and group ACL entries",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "setfacl -m u:root:rwx,u:daemon:r-x,g:root:r--,g:wheel:rw- testfile" 0 "set multi ACL"
        output=$(getfacl testfile 2>&1)
        rlRun "echo \\"\\$output\\" | grep -q 'user:root:rwx'" 0 "user root"
        rlRun "echo \\"\\$output\\" | grep -q 'user:daemon:r-x'" 0 "user daemon"
        rlRun "echo \\"\\$output\\" | grep -q 'group:root:r--'" 0 "group root"
        rlRun "echo \\"\\$output\\" | grep -q 'group:wheel:rw-'" 0 "group wheel" """,
    ),
    (
        "test_acl_setfacl_export_and_restore",
        "setfacl - export ACL and restore",
        "export and restore ACL",
        'rlRun "mkdir testdir" 0 "Create test directory"',
        """rlRun "touch testfile" 0 "Create test file"
        rlRun "setfacl -m u:root:rwx,g:root:rwx testfile" 0 "set ACL"
        rlRun "getfacl -R testdir > acl_backup.txt" 0 "export ACL"
        rlRun "setfacl -b testfile" 0 "clear ACL"
        rlRun "setfacl --restore acl_backup.txt" 0 "restore ACL" """,
    ),
    (
        "test_acl_setfacl_test_dry_run",
        "setfacl --test dry run does not modify ACL",
        "--test dry run does not modify ACL",
        'rlRun "touch testfile" 0 "Create test file"',
        """rlRun "getfacl testfile > before.txt 2>&1" 0 "capture before"
        rlRun "setfacl --test -m u:root:rwx,g:root:--- testfile" 0 "setfacl --test"
        rlRun "getfacl testfile > after.txt 2>&1" 0 "capture after"
        rlRun "diff -u before.txt after.txt" 0 "--test does not modify ACL" """,
    ),
]


# ============================================================
# Generation
# ============================================================

def generate():
    # Delete old test directories (keep only new ones)
    old_dirs = [
        "test_acl_getfacl_basic", "test_acl_setfacl_basic",
        "test_acl_setfacl_advanced", "test_acl_setfacl_remove",
        "test_acl_setfacl_recursive", "test_acl_setfacl_backup_restore",
        "test_acl_setfacl_symlink", "test_acl_acl_inheritance",
        "test_acl_acl_permission_verify", "test_acl_chacl_command",
        "test_acl_default_named_entries", "test_acl_error_handling",
        "test_acl_special_cases",
    ]

    for d in old_dirs:
        path = os.path.join(ACL, d)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"  Deleted old: {d}")

    # Remove lib.sh (package now managed by tmt require)
    lib_path = os.path.join(ACL, "lib.sh")
    if os.path.exists(lib_path):
        os.remove(lib_path)
        print("  Deleted: lib.sh")

    # Generate new test directories
    for dirname, desc_en, desc_zh, setup_extra, test_body in CHECKPOINTS:
        dir_path = os.path.join(ACL, dirname)
        os.makedirs(dir_path, exist_ok=True)

        # Use inspect.cleandoc for proper dedenting: handles first-line-after-opening-quotes
        # that has zero indent (textwrap.dedent fails) and nested if/else/fi blocks.
        setup_text = inspect.cleandoc(setup_extra)
        test_text = inspect.cleandoc(test_body)
        # No-op if already clean, then re-indent by 8 spaces for beakerlib depth
        setup_indented = textwrap.indent(setup_text, '        ') if setup_text else ''
        test_indented = textwrap.indent(test_text, '        ')

        content = HEADER.format(
            desc_en=desc_en,
            desc_zh=desc_zh,
            setup_extra=setup_indented,
            test_body=test_indented,
        )
        test_sh = os.path.join(dir_path, "test.sh")
        with open(test_sh, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        # Mark executable on Linux filesystem and in git index
        try:
            os.chmod(test_sh, os.stat(test_sh).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        except OSError:
            pass  # Windows ignores exec bits
        try:
            subprocess.run(
                ["git", "update-index", "--chmod=+x", test_sh],
                cwd=BASE, capture_output=True, check=False,
            )
        except Exception:
            pass

        # Generate main.fmf
        fmf_content = FMF.format(desc_en=desc_en, dirname=dirname)
        with open(os.path.join(dir_path, "main.fmf"), "w", encoding="utf-8", newline="\n") as f:
            f.write(fmf_content)

        print(f"  Created: {dirname}")

    print(f"\nTotal: {len(CHECKPOINTS)} test cases generated")


if __name__ == "__main__":
    generate()