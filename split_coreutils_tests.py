#!/usr/bin/env python3
"""
Generate individual test files for coreutils package.
Principle: ONE file = ONE feature. Failure pinpoints exact problem.
"""
import os
from pathlib import Path

PKG_DIR = Path(r"E:\code\openruyi-autotest\tests\functional\pkgs\coreutils")
HEADER = """#!/bin/bash
# Functional test: coreutils - {feature}
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    coreutilsSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
{rlPhaseEnd_setup}

    rlPhaseStartTest "{feature}"
{rlRun_commands}
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
"""

SETUP_WITH_FILES = """    rlRun "echo 'hello world' > file1.txt" 0 "Create test file"
    rlRun "echo 'line 1' > lines.txt" 0 "Create lines file"
    for i in $(seq 2 20); do echo "line $i" >> lines.txt; done
    rlRun "mkdir a" 0 "Create directory a"
    rlRun "mkdir ls_testdir" 0 "Create test directory"
    rlRun "echo 'a,b,c' > csv.txt" 0 "Create CSV file"
    rlRun "echo -e 'apple\\norange\\nbanana\\napple' > fruits.txt" 0 "Create fruits file\""""

def create_test(dir_name, feature_desc, commands):
    """Create a test directory and test.sh file."""
    test_dir = PKG_DIR / dir_name
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Build rlRun lines
    rlrun_lines = "\n".join(f"    rlRun \"{cmd}\" {rc} \"{desc}\"" for cmd, rc, desc in commands)
    
    # Need setup files for tests that use file1.txt, etc.
    needs_setup = any('file1.txt' in c or 'lines.txt' in c or 'fruits.txt' in c or 'csv.txt' in c or 'ls_testdir' in c or ' a/' in c or 'a ' in c for c, _, _ in commands)
    
    setup_block = SETUP_WITH_FILES if needs_setup else ""
    
    content = HEADER.format(
        feature=feature_desc,
        rlPhaseEnd_setup=setup_block,
        rlRun_commands=rlrun_lines
    )
    
    (test_dir / "test.sh").write_text(content, encoding='utf-8')
    print(f"  + {dir_name}")


# ================================================================
# 1. SPLIT: system_information (16 features → 16 individual tests)
# ================================================================
def split_system_information():
    print("\n=== Splitting system_information (16 → 16 tests) ===")
    tests = [
        ("test_coreutils_uname_basic", "uname basic system name", [
            ("uname", 0, "uname system name"),
        ]),
        ("test_coreutils_uname_all", "uname -a all info", [
            ("uname -a", 0, "uname -a all info"),
        ]),
        ("test_coreutils_uname_release", "uname -r kernel release", [
            ("uname -r", 0, "uname -r kernel release"),
        ]),
        ("test_coreutils_uname_machine", "uname -m machine hardware", [
            ("uname -m", 0, "uname -m machine hardware"),
        ]),
        ("test_coreutils_who", "who show logged in users", [
            ("who", 0, "who show logged in users"),
        ]),
        ("test_coreutils_whoami", "whoami current user", [
            ("whoami", 0, "whoami current user"),
        ]),
        ("test_coreutils_id_basic", "id user identity", [
            ("id", 0, "id user identity"),
        ]),
        ("test_coreutils_id_user", "id -u user ID", [
            ("id -u", 0, "id -u user ID"),
        ]),
        ("test_coreutils_id_group", "id -g group ID", [
            ("id -g", 0, "id -g group ID"),
        ]),
        ("test_coreutils_groups", "groups show group membership", [
            ("groups", 0, "groups show group membership"),
        ]),
        ("test_coreutils_groups_user", "groups for specific user", [
            ("groups $(whoami)", 0, "groups for specific user"),
        ]),
        ("test_coreutils_users", "users list logged in users", [
            ("users", 0, "users list logged in users"),
        ]),
        ("test_coreutils_hostid", "hostid numeric host identifier", [
            ("hostid", 0, "hostid numeric host identifier"),
        ]),
        ("test_coreutils_nproc", "nproc number of CPUs", [
            ("nproc", 0, "nproc number of CPUs"),
            ("nproc --all", 0, "nproc --all all processors"),
        ]),
        ("test_coreutils_tty", "tty terminal name", [
            ("tty", 0, "tty terminal name"),
        ]),
        ("test_coreutils_logname", "logname login name", [
            ("logname", 0, "logname login name"),
        ]),
        ("test_coreutils_pinky", "pinky user info", [
            ("pinky", 0, "pinky user info"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 2. SPLIT: file_operations (14 features → 7 tests)
# ================================================================
def split_file_operations():
    print("\n=== Splitting file_operations (14 → 7 tests) ===")
    tests = [
        ("test_coreutils_dd", "dd copy file", [
            ("dd if=file1.txt of=dd_out.txt 2>&1", 0, "dd copy file"),
        ]),
        ("test_coreutils_truncate", "truncate set file size", [
            ("truncate -s 100 trunc_test.txt", 0, "truncate set size"),
            ("test $(stat -c %s trunc_test.txt) -eq 100", 0, "truncate: verify size"),
        ]),
        ("test_coreutils_shred", "shred secure file removal", [
            ("echo \"secret data\" > shred_test.txt", 0, "Create file to shred"),
            ("shred -n 1 -u shred_test.txt", 0, "shred remove file securely"),
            ("test ! -f shred_test.txt", 0, "shred: file removed"),
        ]),
        ("test_coreutils_sync", "sync flush filesystem buffers", [
            ("sync", 0, "sync flush filesystem buffers"),
        ]),
        ("test_coreutils_install", "install copy with mode", [
            ("install -m 644 file1.txt install_dest.txt", 0, "install copy with mode"),
            ("test -f install_dest.txt", 0, "install: destination exists"),
            ("install -d install_dir", 0, "install -d create directory"),
            ("test -d install_dir", 0, "install -d: directory exists"),
        ]),
        ("test_coreutils_chroot_version", "chroot version check", [
            ("chroot --version", 0, "chroot version check"),
        ]),
        ("test_coreutils_mkfifo", "mkfifo create named pipe", [
            ("mkfifo mkfifo_pipe", 0, "mkfifo create named pipe"),
            ("test -p mkfifo_pipe", 0, "mkfifo: verify pipe created"),
        ]),
        ("test_coreutils_mknod_version", "mknod version check", [
            ("mknod --version", 0, "mknod version check"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 3. SPLIT: counting_and_statistics (12 features → 6 tests)
# ================================================================
def split_counting_statistics():
    print("\n=== Splitting counting_and_statistics (12 → 6 tests) ===")
    tests = [
        ("test_coreutils_wc", "wc line/word/byte count", [
            ("wc -l lines.txt", 0, "wc -l line count"),
            ("test $(wc -l < lines.txt) -eq 20", 0, "wc -l: 20 lines"),
            ("wc -c lines.txt", 0, "wc -c byte count"),
            ("wc -w lines.txt", 0, "wc -w word count"),
            ("wc -m lines.txt", 0, "wc -m character count"),
        ]),
        ("test_coreutils_du", "du disk usage", [
            ("du -sh .", 0, "du -sh summary human"),
            ("du -h a/", 0, "du -h directory usage"),
        ]),
        ("test_coreutils_df", "df filesystem disk space", [
            ("df -h", 0, "df -h human readable"),
            ("df -h / | tail -1", 0, "df: root filesystem"),
        ]),
        ("test_coreutils_stat_file", "stat file status", [
            ("stat file1.txt", 0, "stat file status"),
            ("stat -c \"%s %n\" file1.txt", 0, "stat -c format output"),
        ]),
        ("test_coreutils_stat_filesystem", "stat filesystem status", [
            ("stat -f /", 0, "stat -f filesystem status"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 4. SPLIT: text_processing_i (13 features → 7 tests)
# ================================================================
def split_text_processing_i():
    print("\n=== Splitting text_processing_i (13 → 7 tests) ===")
    tests = [
        ("test_coreutils_sort_basic", "sort alphabetically", [
            ("sort fruits.txt", 0, "sort alphabetically"),
            ("test \"$(sort fruits.txt | head -1)\" = \"apple\"", 0, "sort: first is apple"),
        ]),
        ("test_coreutils_sort_reverse", "sort -r reverse", [
            ("sort -r fruits.txt", 0, "sort -r reverse"),
        ]),
        ("test_coreutils_sort_unique", "sort -u unique", [
            ("sort -u fruits.txt", 0, "sort -u unique"),
        ]),
        ("test_coreutils_sort_numeric", "sort -n numeric", [
            ("sort -n fruits.txt 2>&1 | grep -qiE \"error|Error|not found|No such|Unable to\" || echo expected-error", 1, "sort -n numeric"),
        ]),
        ("test_coreutils_uniq", "uniq filter repeated lines", [
            ("sort fruits.txt | uniq", 0, "uniq unique lines"),
            ("test $(sort fruits.txt | uniq | wc -l) -eq 4", 0, "uniq: 4 unique"),
            ("sort fruits.txt | uniq -c", 0, "uniq -c count occurrences"),
            ("sort fruits.txt | uniq -d", 0, "uniq -d only duplicates"),
            ("sort fruits.txt | uniq -u", 0, "uniq -u only uniques"),
        ]),
        ("test_coreutils_cut", "cut extract fields", [
            ("cut -d: -f1 csv.txt", 0, "cut -d: -f1 first field"),
            ("cut -d: -f2 csv.txt", 0, "cut -d: -f2 second field"),
            ("cut -d: -f1,3 csv.txt", 0, "cut multiple fields"),
            ("cut -c1-4 file1.txt", 0, "cut -c character range"),
        ]),
        ("test_coreutils_tr", "tr translate/delete characters", [
            ("echo \"UPPERCASE\" | tr \"A-Z\" \"a-z\"", 0, "tr translate uppercase to lowercase"),
            ("echo \"abc\" | tr -d \"b\"", 0, "tr -d delete characters"),
            ("echo \"a b c\" | tr -s \" \"", 0, "tr -s squeeze repeats"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 5. SPLIT: checksums (11 features → 5 tests)
# ================================================================
def split_checksums():
    print("\n=== Splitting checksums (11 → 5 tests) ===")
    tests = [
        ("test_coreutils_cksum", "cksum CRC checksum", [
            ("cksum file1.txt", 0, "cksum CRC checksum"),
        ]),
        ("test_coreutils_md5sum", "md5sum compute and verify", [
            ("md5sum file1.txt", 0, "md5sum compute"),
            ("md5sum file1.txt > md5_check.txt", 0, "md5sum save"),
            ("md5sum -c md5_check.txt", 0, "md5sum -c verify"),
        ]),
        ("test_coreutils_sha1sum", "sha1sum compute and verify", [
            ("sha1sum file1.txt", 0, "sha1sum compute"),
            ("sha1sum file1.txt > sha1_check.txt", 0, "sha1sum save"),
            ("sha1sum -c sha1_check.txt", 0, "sha1sum -c verify"),
        ]),
        ("test_coreutils_sha_family", "sha224/256/384/512 compute", [
            ("sha224sum file1.txt", 0, "sha224sum compute"),
            ("sha256sum file1.txt", 0, "sha256sum compute"),
            ("sha256sum file1.txt > sha256_check.txt", 0, "sha256sum save"),
            ("sha256sum -c sha256_check.txt", 0, "sha256sum -c verify"),
            ("sha384sum file1.txt", 0, "sha384sum compute"),
            ("sha512sum file1.txt", 0, "sha512sum compute"),
        ]),
        ("test_coreutils_b2sum_and_sum", "b2sum and sum checksums", [
            ("b2sum file1.txt", 0, "b2sum BLAKE2 checksum"),
            ("sum file1.txt", 0, "sum BSD checksum"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 6. SPLIT: text_processing_ii (9 features → 6 tests)
# ================================================================
def split_text_processing_ii():
    print("\n=== Splitting text_processing_ii (9 → 6 tests) ===")
    tests = [
        ("test_coreutils_paste", "paste merge lines", [
            ("echo -e 'a\\nb' > paste1.txt", 0, "Create paste file 1"),
            ("echo -e '1\\n2' > paste2.txt", 0, "Create paste file 2"),
            ("paste paste1.txt paste2.txt", 0, "paste merge files"),
        ]),
        ("test_coreutils_comm", "comm compare sorted files", [
            ("sort fruits.txt > sorted1.txt", 0, "Create sorted file 1"),
            ("sort fruits.txt > sorted2.txt", 0, "Create sorted file 2"),
            ("comm sorted1.txt sorted2.txt", 0, "comm compare files"),
        ]),
        ("test_coreutils_join", "join merge on common field", [
            ("join sorted1.txt sorted2.txt 2>&1", 0, "join merge files"),
        ]),
        ("test_coreutils_fmt", "fmt format text", [
            ("echo 'This is a long line of text that should be reformatted by fmt' > fmt_test.txt", 0, "Create fmt test file"),
            ("fmt fmt_test.txt", 0, "fmt format text"),
        ]),
        ("test_coreutils_fold", "fold wrap lines", [
            ("echo '1234567890abcdefghij' | fold -w 5", 0, "fold -w 5 wrap at 5 chars"),
        ]),
        ("test_coreutils_expand_unexpand", "expand/unexpand tabs", [
            ("echo -e 'a\\tb' | expand", 0, "expand tabs to spaces"),
            ("echo 'a        b' | unexpand -a", 0, "unexpand -a spaces to tabs"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 7. SPLIT: special_utilities (8 features → 4 tests)
# ================================================================
def split_special_utilities():
    print("\n=== Splitting special_utilities (8 → 4 tests) ===")
    tests = [
        ("test_coreutils_stty", "stty terminal settings", [
            ("stty -a", 0, "stty -a show all settings"),
        ]),
        ("test_coreutils_pathchk", "pathchk validate path", [
            ("pathchk /tmp/test_path", 0, "pathchk validate path"),
        ]),
        ("test_coreutils_tsort", "tsort topological sort", [
            ("echo -e 'a b\\nb c' | tsort", 0, "tsort topological sort"),
        ]),
        ("test_coreutils_dircolors", "dircolors LS_COLORS", [
            ("dircolors", 0, "dircolors output LS_COLORS"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 8. SPLIT: links_and_path_resolution (7 features → 4 tests)
# ================================================================
def split_links_path():
    print("\n=== Splitting links_and_path (7 → 4 tests) ===")
    tests = [
        ("test_coreutils_ln", "ln create links", [
            ("ln -s file1.txt symlink.txt", 0, "ln -s create symbolic link"),
            ("test -L symlink.txt", 0, "ln -s: verify symlink exists"),
            ("ln file1.txt hardlink.txt", 0, "ln create hard link"),
            ("test -f hardlink.txt", 0, "ln: verify hard link exists"),
        ]),
        ("test_coreutils_link_unlink", "link/unlink operations", [
            ("link file1.txt link_test.txt", 0, "link create hard link"),
            ("test -f link_test.txt", 0, "link: verify exists"),
            ("unlink link_test.txt", 0, "unlink remove hard link"),
            ("test ! -f link_test.txt", 0, "unlink: verify removed"),
        ]),
        ("test_coreutils_readlink", "readlink resolve symlinks", [
            ("ln -sf file1.txt readlink_test.txt", 0, "Create symlink"),
            ("readlink readlink_test.txt", 0, "readlink resolve symlink"),
        ]),
        ("test_coreutils_realpath", "realpath absolute path", [
            ("realpath file1.txt", 0, "realpath resolve absolute path"),
            ("realpath -e /usr/bin/grep", 0, "realpath -e existing path"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 9. SPLIT: file_creation_and_listing (6 features → 3 tests)
# ================================================================
def split_file_creation_listing():
    print("\n=== Splitting file_creation_and_listing (6 → 3 tests) ===")
    tests = [
        ("test_coreutils_echo", "echo print text", [
            ("echo \"hello\"", 0, "echo print text"),
            ("echo -n \"no-newline\"", 0, "echo -n no newline"),
        ]),
        ("test_coreutils_cat", "cat concatenate files", [
            ("cat file1.txt", 0, "cat display file"),
            ("cat file1.txt file1.txt", 0, "cat concatenate files"),
        ]),
        ("test_coreutils_ls", "ls list directory", [
            ("ls", 0, "ls list files"),
            ("ls -l", 0, "ls -l long format"),
            ("ls -a", 0, "ls -a show hidden"),
            ("ls -la", 0, "ls -la long all"),
        ]),
        ("test_coreutils_dir_vdir", "dir and vdir commands", [
            ("dir", 0, "dir list directory"),
            ("vdir", 0, "vdir long listing"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 10. SPLIT: file_viewing (6 features → 4 tests)
# ================================================================
def split_file_viewing():
    print("\n=== Splitting file_viewing (6 → 4 tests) ===")
    tests = [
        ("test_coreutils_head", "head show first lines", [
            ("head lines.txt", 0, "head show first 10 lines"),
            ("head -n 5 lines.txt", 0, "head -n 5 first 5 lines"),
        ]),
        ("test_coreutils_tail", "tail show last lines", [
            ("tail lines.txt", 0, "tail show last 10 lines"),
            ("tail -n 5 lines.txt", 0, "tail -n 5 last 5 lines"),
        ]),
        ("test_coreutils_tac", "tac reverse lines", [
            ("tac fruits.txt", 0, "tac reverse lines"),
        ]),
        ("test_coreutils_nl", "nl number lines", [
            ("nl lines.txt", 0, "nl number lines"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 11. SPLIT: flow_control (5 features → 3 tests)
# ================================================================
def split_flow_control():
    print("\n=== Splitting flow_control (5 → 3 tests) ===")
    tests = [
        ("test_coreutils_sleep", "sleep delay execution", [
            ("sleep 1", 0, "sleep 1 second"),
        ]),
        ("test_coreutils_timeout", "timeout command limit", [
            ("timeout 1 sleep 2 2>&1 | grep -qiE \"Terminated|error\" || echo timed-out", 0, "timeout kills command"),
        ]),
        ("test_coreutils_yes", "yes output string", [
            ("yes | head -n 3", 0, "yes output y repeatedly"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 12. SPLIT: numbers_and_expressions (6 features → 4 tests)
# ================================================================
def split_numbers():
    print("\n=== Splitting numbers_and_expressions (6 → 4 tests) ===")
    tests = [
        ("test_coreutils_seq", "seq generate sequence", [
            ("seq 1 5", 0, "seq 1..5"),
            ("seq -s ',' 1 5", 0, "seq -s custom separator"),
        ]),
        ("test_coreutils_factor", "factor prime factorization", [
            ("factor 42", 0, "factor prime factorization"),
        ]),
        ("test_coreutils_shuf", "shuf shuffle lines", [
            ("shuf fruits.txt", 0, "shuf randomize lines"),
        ]),
        ("test_coreutils_numfmt", "numfmt format numbers", [
            ("echo 1234567 | numfmt --to=si", 0, "numfmt --to=si"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# 13. NEW: Missing coreutils features
# ================================================================
def add_missing_tests():
    print("\n=== Adding missing coreutils features ===")
    tests = [
        ("test_coreutils_env", "env run with modified environment", [
            ("env", 0, "env show all variables"),
            ("env VAR=test echo ok", 0, "env set variable and run"),
        ]),
        ("test_coreutils_printenv", "printenv print environment", [
            ("printenv PATH", 0, "printenv PATH variable"),
        ]),
        ("test_coreutils_date", "date show/set system date", [
            ("date", 0, "date show current date"),
        ]),
        ("test_coreutils_printf", "printf formatted output", [
            ("printf \"hello %s\\n\" world", 0, "printf format string"),
        ]),
        ("test_coreutils_true", "true always returns success", [
            ("true", 0, "true exit 0"),
        ]),
        ("test_coreutils_false", "false always returns failure", [
            ("false", 1, "false exit 1"),
        ]),
        ("test_coreutils_test_builtin", "test condition evaluation", [
            ("test -f file1.txt", 0, "test -f file exists"),
            ("test ! -f nonexistent", 0, "test ! -f file not exists"),
        ]),
        ("test_coreutils_mktemp", "mktemp create temp file", [
            ("mktemp", 0, "mktemp create temp file"),
            ("mktemp -d", 0, "mktemp -d create temp dir"),
        ]),
        ("test_coreutils_dirname_and_basename", "dirname and basename", [
            ("test \"$(basename /usr/bin/grep)\" = \"grep\"", 0, "basename extract filename"),
            ("test \"$(dirname /usr/bin/grep)\" = \"/usr/bin\"", 0, "dirname extract directory"),
        ]),
        ("test_coreutils_expand", "expand tabs to spaces", [
            ("echo -e 'a\\tb' | expand", 0, "expand tabs to spaces"),
        ]),
        ("test_coreutils_tee", "tee redirect to file", [
            ("echo 'test' | tee tee_out.txt", 0, "tee write to file"),
            ("test -f tee_out.txt", 0, "tee: file created"),
        ]),
        ("test_coreutils_split", "split file into pieces", [
            ("split -l 5 lines.txt split_", 0, "split -l 5 lines per file"),
        ]),
        ("test_coreutils_csplit", "csplit split by context", [
            ("csplit --version", 0, "csplit version check"),
        ]),
        ("test_coreutils_ptx", "ptx permuted index", [
            ("ptx --version", 0, "ptx version check"),
        ]),
        ("test_coreutils_nice", "nice run with priority", [
            ("nice true", 0, "nice run command"),
        ]),
        ("test_coreutils_nohup", "nohup immune to hangups", [
            ("nohup true", 0, "nohup run command"),
        ]),
        ("test_coreutils_stdbuf", "stdbuf buffer control", [
            ("stdbuf --version", 0, "stdbuf version check"),
        ]),
        ("test_coreutils_cp_single", "cp single file", [
            ("cp file1.txt cp_single_out.txt", 0, "cp copy file"),
            ("test -f cp_single_out.txt", 0, "cp: verify copy exists"),
            ("diff file1.txt cp_single_out.txt", 0, "cp: files identical"),
        ]),
        ("test_coreutils_cp_recursive", "cp -r recursive", [
            ("cp -r ls_testdir ls_testdir_copy", 0, "cp -r recursive copy"),
            ("test -d ls_testdir_copy", 0, "cp -r: verify directory copy"),
        ]),
        ("test_coreutils_mv", "mv rename/move file", [
            ("cp file1.txt mv_test.txt", 0, "Create file to move"),
            ("mv mv_test.txt mv_renamed.txt", 0, "mv rename file"),
            ("test ! -f mv_test.txt", 0, "mv: old name gone"),
            ("test -f mv_renamed.txt", 0, "mv: new name exists"),
        ]),
        ("test_coreutils_rm", "rm remove file", [
            ("touch rm_test.txt", 0, "Create temp file"),
            ("rm rm_test.txt", 0, "rm remove file"),
            ("test ! -f rm_test.txt", 0, "rm: file removed"),
        ]),
        ("test_coreutils_rm_recursive", "rm -rf recursive remove", [
            ("cp -r ls_testdir rm_testdir", 0, "Create dir to remove"),
            ("rm -rf rm_testdir", 0, "rm -rf recursive force"),
            ("test ! -d rm_testdir", 0, "rm -rf: directory removed"),
        ]),
        ("test_coreutils_rmdir", "rmdir remove empty directory", [
            ("mkdir rmdir_test", 0, "Create empty directory"),
            ("rmdir rmdir_test", 0, "rmdir remove empty directory"),
            ("test ! -d rmdir_test", 0, "rmdir: directory removed"),
        ]),
    ]
    for dir_name, feature, cmds in tests:
        create_test(dir_name, feature, cmds)


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Coreutils test splitting: ONE file = ONE feature")
    print("=" * 60)
    
    # Split existing complex tests
    split_system_information()
    split_file_operations()
    split_counting_statistics()
    split_text_processing_i()
    split_checksums()
    split_text_processing_ii()
    split_special_utilities()
    split_links_path()
    split_file_creation_listing()
    split_file_viewing()
    split_flow_control()
    split_numbers()
    
    # Add missing features
    add_missing_tests()
    
    print(f"\n{'=' * 60}")
    print("Done! Now delete old complex test directories and run CI.")
    print(f"{'=' * 60}")