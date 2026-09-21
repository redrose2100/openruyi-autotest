#!/usr/bin/env python3
"""
Fix generated tests: add missing rlPhaseEnd after setup, and remove duplicates.
Also split remaining old multi-feature tests.
"""
import os, re
from pathlib import Path

PKG_DIR = Path(r"E:\code\openruyi-autotest\tests\functional\pkgs\coreutils")

HEADER_FIXED = """#!/bin/bash
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
    rlPhaseEnd

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

def fix_test_file(test_dir):
    """Fix a generated test file: ensure rlPhaseEnd is present after setup."""
    test_sh = test_dir / "test.sh"
    if not test_sh.exists():
        return
    content = test_sh.read_text(encoding='utf-8')
    
    # Check if rlPhaseEnd already exists after setup (before rlPhaseStartTest)
    if 'rlPhaseEnd\n\n    rlPhaseStartTest' in content:
        return  # Already fixed
    
    # Add rlPhaseEnd after setup block, before rlPhaseStartTest
    old = content
    content = content.replace('\n    rlPhaseStartTest', '\n    rlPhaseEnd\n\n    rlPhaseStartTest')
    if content != old:
        test_sh.write_text(content, encoding='utf-8')
        print(f"  FIXED: {test_dir.name}")

def create_test(dir_name, feature_desc, commands):
    test_dir = PKG_DIR / dir_name
    test_dir.mkdir(parents=True, exist_ok=True)
    
    rlrun_lines = "\n".join(f"    rlRun \"{cmd}\" {rc} \"{desc}\"" for cmd, rc, desc in commands)
    needs_setup = any('file1.txt' in c or 'lines.txt' in c or 'fruits.txt' in c or 'csv.txt' in c or 'ls_testdir' in c or ' a/' in c or 'a ' in c for c, _, _ in commands)
    setup_block = SETUP_WITH_FILES if needs_setup else ""
    
    content = HEADER_FIXED.format(
        feature=feature_desc,
        rlPhaseEnd_setup=setup_block,
        rlRun_commands=rlrun_lines
    )
    (test_dir / "test.sh").write_text(content, encoding='utf-8')
    print(f"  + {dir_name}")

# Fix all existing test files
print("=== Fixing missing rlPhaseEnd in generated tests ===")
for d in sorted(PKG_DIR.iterdir()):
    if d.is_dir() and d.name.startswith('test_'):
        fix_test_file(d)

# Remove duplicates and old multi-feature dirs
print("\n=== Removing duplicates and old multi-feature dirs ===")
to_remove = [
    "test_coreutils_redirection__tee",      # -> test_coreutils_tee
    "test_coreutils_split_files__split__csplit",  # -> test_coreutils_split, test_coreutils_csplit
    "test_coreutils_process_control__nice__nohup__stdbuf",  # -> new individual tests
]
for d in to_remove:
    path = PKG_DIR / d
    if path.exists():
        import shutil
        shutil.rmtree(str(path))
        print(f"  REMOVED: {d}")

# Split remaining old multi-feature tests
print("\n=== Splitting remaining old tests ===")

# Split: boolean_and_condition__true__false__test
old_d = PKG_DIR / "test_coreutils_boolean_and_condition__true__false__test"
if old_d.exists():
    create_test("test_coreutils_test_eval", "test [ ] expression evaluation", [
        ("[ -f file1.txt ]", 0, "test -f file exists"),
        ("[ ! -f nonexistent ]", 0, "test ! -f file not exists"),
        ("[ 1 -eq 1 ]", 0, "test numeric equality"),
    ])
    # true and false already created above
    import shutil; shutil.rmtree(str(old_d))
    print("  REMOVED: test_coreutils_boolean_and_condition__true__false__test")

# Split: path_operations (already have some new tests, just remove old)
old_d = PKG_DIR / "test_coreutils_path_operations__basename__dirname__pwd"
if old_d.exists():
    import shutil; shutil.rmtree(str(old_d))
    print("  REMOVED: test_coreutils_path_operations__basename__dirname__pwd")

# Split: encoding (base32/base64/basenc)
old_d = PKG_DIR / "test_coreutils_encoding__base32__base64__basenc"
if old_d.exists():
    create_test("test_coreutils_base32", "base32 encode/decode", [
        ("echo 'hello' | base32", 0, "base32 encode"),
        ("echo 'hello' | base32 | base32 -d", 0, "base32 -d decode"),
    ])
    create_test("test_coreutils_base64", "base64 encode/decode", [
        ("echo 'hello' | base64", 0, "base64 encode"),
        ("echo 'hello' | base64 | base64 -d", 0, "base64 -d decode"),
    ])
    create_test("test_coreutils_basenc", "basenc base64 encoding", [
        ("echo 'hello' | basenc --base64", 0, "basenc --base64 encode"),
    ])
    import shutil; shutil.rmtree(str(old_d))
    print("  REMOVED: test_coreutils_encoding__base32__base64__basenc")

# Split: octal_dump__od (already small, just rename to simpler name)
old_d = PKG_DIR / "test_coreutils_octal_dump__od"
if old_d.exists():
    create_test("test_coreutils_od", "od octal dump", [
        ("od file1.txt", 0, "od octal dump"),
        ("od -c file1.txt", 0, "od -c character dump"),
        ("od -x file1.txt", 0, "od -x hex dump"),
        ("od -A x file1.txt", 0, "od -A x hex address"),
    ])
    import shutil; shutil.rmtree(str(old_d))
    print("  REMOVED: test_coreutils_octal_dump__od")

print("\nDone! All tests now follow: ONE file = ONE feature point.")