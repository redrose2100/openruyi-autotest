# openruyi-autotest Development Guide

> How to contribute new test cases to openruyi-autotest.
>
> **Related Documents**: [Commit & MR Standards](commit_guide.md) · [User Guide](user_guide.md)

---

## 1. Test Framework Overview

openruyi-autotest is based on the [tmt (Test Management Tool)](https://tmt.readthedocs.io/) framework, using [BeakerLib](https://github.com/beakerlib/beakerlib) for test scripts and [FMF (Flexible Metadata Format)](https://fmf.readthedocs.io/) for metadata management.

### Core Concepts

| Concept | Description | File |
|---------|-------------|------|
| **Test Plan** | Defines how to discover, prepare, execute, and report tests | `plans/*.fmf` |
| **Test Case** | Concrete test script + metadata | `tests/**/test.sh` + `main.fmf` |
| **FMF Metadata** | YAML-formatted test description | `main.fmf` |
| **BeakerLib** | Shell test framework providing rlRun/rlAssertGrep etc. | Source `. /usr/share/beakerlib/beakerlib.sh` |

---

## 2. Directory Conventions

```
tests/
├── main.fmf                     # Global shared config (framework, duration, etc.)
├── smoke/                       # Smoke tests
│   ├── main.fmf                 # Smoke-level shared config
│   └── <category>/              # Category directory
│       ├── main.fmf             # Category shared config
│       ├── lib.sh               # Category-level shared library (optional)
│       └── test_smoke_<name>/   # Test case directory
│           ├── main.fmf         # Case metadata
│           └── test.sh          # Case script
├── functional/                  # Functional tests
│   ├── main.fmf                 # Functional-level shared config
│   └── pkgs/                    # RPM package tests
│       └── <pkg>/               # Package directory
│           ├── main.fmf         # Package-level metadata
│           ├── lib.sh           # Package-level shared library (optional)
│           └── test_<pkg>_<feature>/  # Functional test case
│               ├── main.fmf
│               └── test.sh
├── security/                    # Security tests
├── compatibility/               # Compatibility tests
├── performance/                 # Performance tests
├── feature/                     # Feature tests
│   ├── main.fmf                 # Feature-level shared config
│   └── <xxx>/                   # Feature name (e.g. gpu, network)
│       ├── main.fmf             # Feature-level metadata
│       └── test_feature_<aaa>/  # Feature test case (aaa = specific description)
│           ├── main.fmf
│           └── test.sh
└── reliability/                 # Reliability tests
```

---

## 3. Adding a New Test Case

### 3.1 Create Directories and Files

Example: adding a new test case under the acl package:

```bash
# 1. Create test case directory
mkdir -p tests/functional/pkgs/acl/test_acl_my_feature

# 2. Create metadata file
cat > tests/functional/pkgs/acl/test_acl_my_feature/main.fmf << 'EOF'
summary: Functional Test - acl - my feature
test: ./test.sh
framework: shell
tag:
  - functional
  - acl
duration: 2m
tier: 1
path: /tests/functional/pkgs/acl/test_acl_my_feature
require:
  - acl
  - coreutils
  - beakerlib
EOF
```

> **Field notes**: `framework: shell` declares the Shell test framework; `tag: [functional, acl]` ensures discovery by the functional plan; `duration` can override parent defaults; `require` needs the package under test plus `coreutils` (basic file/directory ops) and `beakerlib` (test framework).

### 3.2 Writing Test Scripts

```bash
cat > tests/functional/pkgs/acl/test_acl_my_feature/test.sh << 'TESTEOF'
#!/bin/bash
# Functional test: acl - my feature
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment Setup"
        aclSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "touch testfile" 0 "Create test file"
        rlRun "mkdir testdir" 0 "Create test directory"
    rlPhaseEnd

    rlPhaseStartTest "My Feature Test"
        # Feature 1: Basic verification
        rlRun "getfacl testfile" 0 "View default ACL of file"

        # Feature 2: Set ACL
        rlRun "setfacl -m u:root:rwx testfile" 0 "Set user ACL"
        rlRun "getfacl testfile 2>&1 | grep -q 'user:root:rwx'" 0 "Confirm ACL is set"
    rlPhaseEnd

    rlPhaseStartCleanup "Cleanup Test Environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
        # acl package auto-uninstalled by lib.sh reference counting
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
TESTEOF
```

> **`rlRun` exit code rules**: The second parameter `0` means the command is expected to succeed (exit code 0), `1` means the command is expected to fail (used for negative testing). If the actual exit code does not match, rlRun reports FAIL and prevents subsequent phase execution.

### 3.3 BeakerLib Lifecycle

Each test script follows the standard three-phase structure:

| Phase | Function | Purpose |
|-------|----------|---------|
| **Setup** | `rlPhaseStartSetup` | Environment preparation: install packages, create temp directories, call `*Setup()` shared library functions |
| **Test** | `rlPhaseStartTest` | Execute tests: call commands under test, assert results. Can have multiple phases, one feature per test |
| **Cleanup** | `rlPhaseStartCleanup` | Clean up environment: remove temp files, return to original directory; shared library auto-manages package uninstall |

> **Note**: The `aclSetup()` called in `rlPhaseStartSetup` registers a cleanup callback via `rlCleanupAppend`, so the Cleanup phase does **not** need to manually uninstall packages.

### 3.3.1 How Are Tests Discovered by tmt?

The tmt execution flow is: the Plan's `discover` phase traverses the `tests/` directory tree and matches tests using FMF `tag` filtering.

```
tmt run plan --name /plans/functional
  │
  ├─ [discover] plans/functional.fmf → filter: "tag:functional"
  │   │
  │   ├─ Traverse tests/ tree, match all main.fmf with tag "functional"
  │   │  ✓ tests/functional/pkgs/acl/test_acl_getfacl_basic/main.fmf
  │   │  ✓ tests/functional/pkgs/acl/test_acl_setfacl_basic/main.fmf
  │   │  ✗ tests/smoke/archive/main.fmf              (tag: smoke)
  │   │  ✗ tests/security/cve/main.fmf               (tag: security)
  │   │
  │   └─ Output: 202 tests discovered
  │
  ├─ [execute] Execute each test.sh in order
  │
  └─ [report] Summarize results
```

**Key points**:
- `main.fmf` must include `tag: [functional]` (or the corresponding plan tag) to be discovered by the plan
- Plan files (e.g. `plans/functional.fmf`) declare matching conditions via `filter: "tag:functional"`
- Different plans can run the same test set (just add multiple tags)
- Tag names come from test type names: `smoke`, `functional`, `security`, `compatibility`, `performance`, `reliability`, `feature`

### 3.4 Shared Library (lib.sh)

When multiple test cases under the same package need to share install/uninstall logic, use `lib.sh`.

**Design points**:

- **`library-prefix` annotation**: The header `# library-prefix = acl` declares the function prefix; all public functions start with `acl`.
- **Reference counting**: Uses a flag file (e.g. `/tmp/.beakerlib_acl_suite`) to track how many test cases are using the suite. The first test installs the package, the last one uninstalls.
- **`rlCleanupAppend`**: Registers the cleanup function during Setup; BeakerLib automatically calls it at `rlJournalEnd` regardless of test success/failure.
- **`sudo` handling**: The project uses `echo <password> | sudo -S <cmd>` for sudo password injection; install/uninstall commands in `lib.sh` need to adapt.

**`lib.sh` example**:

```bash
# library-prefix = acl
#
# ACL suite-level shared library
# Usage in each test file:
#   . "$(dirname "$0")/../lib.sh"    # from test_acl_xxx/ subdirectories
#
# Then call:  aclSetup   in rlPhaseStartSetup
# The cleanup is auto-registered via rlCleanupAppend.

ACL_FLAG="/tmp/.beakerlib_acl_suite"

aclSetup() {
    if [ ! -f "$ACL_FLAG" ]; then
        if ! rpm -q acl 2>/dev/null; then
            echo openruyi | sudo -S dnf install -y acl 2>/dev/null
            echo "installed=1" > "$ACL_FLAG"
        else
            echo "installed=0" > "$ACL_FLAG"
        fi
        echo "ref=1" >> "$ACL_FLAG"
    else
        local ref=$(grep "^ref=" "$ACL_FLAG" | cut -d= -f2)
        ref=$((ref + 1))
        sed -i "s/^ref=.*/ref=$ref/" "$ACL_FLAG"
    fi
    rlCleanupAppend "aclCleanup"
}

aclCleanup() {
    [ ! -f "$ACL_FLAG" ] && return 0
    local ref=$(grep "^ref=" "$ACL_FLAG" | cut -d= -f2)
    ref=$((ref - 1))
    if [ "$ref" -le 0 ]; then
        grep -q "^installed=1" "$ACL_FLAG" && echo openruyi | sudo -S dnf remove -y acl 2>/dev/null || true
        rm -f "$ACL_FLAG"
    else
        sed -i "s/^ref=.*/ref=$ref/" "$ACL_FLAG"
    fi
}
```

---

## 4. FMF Metadata Field Reference

### Test Case (main.fmf)

| Field | Type | Required | Description |
|-------|------|:---:|------|
| `summary` | string | ✅ | Short test description, format: `Test Type - Package - Feature` |
| `test` | string | ✅ | Test script path, typically `./test.sh` |
| `framework` | string | | Test framework, `shell` for Shell scripts (inherited from `tests/main.fmf`) |
| `tag` | list | ✅ | Tag list, e.g. `[functional, acl]`. Plans match via `filter: "tag:functional"` |
| `duration` | string | ✅ | Estimated run time, e.g. `2m`, `5m`. Can override parent defaults |
| `tier` | int | ✅ | Priority: 0=smoke (per commit), 1=core (daily), 2=extended (pre-release) |
| `path` | string | ✅ | Test path, format `/tests/<type>/pkgs/<pkg>/<test>` |
| `require` | list | ✅ | Dependent RPM packages (must include package under test + `coreutils` + `beakerlib`) |
| `contact` | string | | Test owner/maintainer |
| `environment` | dict | | Custom environment variables, e.g. `{VAR1: val1, VAR2: val2}`, injected into test environment |
| `extra-hardware-require` | dict | | Hardware requirement declaration (see Section 5.3), e.g. `{cpu: ">= 4", memory: ">= 8 GiB"}` |

### Test Plan (plans/*.fmf)

```yaml
summary: Functional test plan
discover:
  how: fmf
  test:
    - /tests/functional
provision:
  how: local
prepare:
  how: shell
  script:
    - echo ""
execute:
  how: tmt
```

---

## 5. Hardware Environment Constraints

All plans in this project use `how: local` mode, implementing hardware environment constraints through **FMF metadata declarations + environment variable injection + shared library self-checks**. When the environment does not satisfy the declaration, tests automatically SKIP (`exit 0`) without blocking other cases.

### 5.1 Component Overview

| Component | File | Purpose |
|-----------|------|---------|
| Topology config template | `topology.env.example` | Repo-level template, committed to version control |
| Topology config instance | `topology.env` | Actual server info, `.gitignore`'d, not committed |
| Test case declaration | `extra-hardware-require` in `main.fmf` | Each case declares its hardware requirements |
| Plan loading | `environment-file` in `plans/*.fmf` | Injects `topology.env` as environment variables |
| Shared check library | `tests/lib/hw_check.sh` | Parses declarations, compares environment, remote execution |

### 5.2 Topology Configuration (`topology.env`)

Copy from `topology.env.example` to `topology.env` and modify for your environment:

```bash
TEST_SERVER_COUNT=2
TEST_SERVER_1_HOST=10.20.237.192
TEST_SERVER_1_PORT=12055
TEST_SERVER_1_USER=openruyi
TEST_SERVER_1_PASSWORD=openruyi
TEST_SERVER_2_HOST=10.20.238.100
TEST_SERVER_2_PORT=22
TEST_SERVER_2_USER=openruyi
TEST_SERVER_2_PASSWORD=openruyi
```

### 5.3 Test Case Declaration (`extra-hardware-require`)

#### Supported Fields

| Field | Meaning | Check Method | Example Value |
|-------|---------|--------------|---------------|
| `server` | Number of servers needed | Compare with `TEST_SERVER_COUNT` | `2` |
| `cpu` | CPU cores per server | `nproc` | `">= 4"` |
| `memory` | Available memory per server | `free -g` | `">= 8 GiB"` |
| `disk` | Disk count per server | `lsblk -nd` | `">= 1"` |
| `net` | UP network interfaces per server | `ip -o link show` | `">= 1"` |

Supported comparison operators: `=` `!=` `>=` `<=` `>` `<`

#### Hierarchical Inheritance

Use FMF's hierarchical inheritance to declare defaults at the test type parent level; child suites don't need to repeat:

```
tests/functional/main.fmf          ← extra-hardware-require (defaults)
  └─ pkgs/acl/main.fmf              ← No extra-hardware-require → inherits parent
  │    ├─ test_acl_getfacl_basic/    → Gets defaults ✅
  │    └─ test_acl_setfacl/          → Gets defaults ✅
  └─ kernel/realtime/main.fmf       ← cpu: ">= 16" → overrides cpu
       └─ test_rt_latency/           → cpu>=16, rest inherited ✅
```

#### Current Defaults

All test type parents `tests/*/main.fmf` have unified declarations:

```yaml
extra-hardware-require:
  server: 1
  cpu: ">= 4"
  memory: ">= 8 GiB"
  disk: ">= 1"
  net: ">= 1"
```

#### Override on Demand

Child suites only override fields that need elevation; the rest are automatically inherited:

```yaml
# tests/functional/kernel/realtime/main.fmf
extra-hardware-require:
  cpu: ">= 16"        # Overrides parent's ">= 4"
  memory: ">= 16 GiB"  # Overrides parent's ">= 8 GiB"
  # server/disk/net not written, auto-inherited from parent defaults
```

### 5.4 Shared Library Functions (`tests/lib/hw_check.sh`)

Include the shared library in test scripts and call:

```bash
. "$(dirname "$0")/../../lib/hw_check.sh"
```

| Function | Purpose |
|----------|---------|
| `hwVerify [fmf]` | Comprehensive check of all fields; `exit 0` (tmt treats as skip) if not met |
| `hwServerVerify [fmf]` | Check server count only |
| `hwCpuCheck [fmf]` | Check CPU cores only |
| `hwMemCheck [fmf]` | Check memory size only |
| `hwDiskCheck [fmf]` | Check disk count only |
| `hwNetCheck [fmf]` | Check network interfaces (UP state, excluding lo) only |
| `hwRunOnServer <idx> <cmd>` | Execute command remotely on specified server index |
| `hwGetServerInfo <idx> <field>` | Get server connection info (`host`/`port`/`user`/`password`) |

### 5.5 Plan Configuration

All `how: local` plans must add `environment-file` to load topology environment variables:

```yaml
# plans/functional.fmf
environment-file:
  - topology.env
```

All project plan files are already configured: `functional`, `smoke`, `security`, `performance`, `reliability`, `compatibility`, `feature`, `all`.

### 5.6 Complete Test Case Example

**`main.fmf`**:

```yaml
summary: Functional Test - my_pkg - multi-server failover
test: ./test.sh
tag:
  - functional
  - my_pkg
duration: 5m
tier: 2
extra-hardware-require:
  server: 2
```

**`test.sh`**:

```bash
#!/bin/bash
# Functional test: my_pkg - multi-server failover
# Requires 2 servers; auto-skips if topology.env has fewer

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../../lib/hw_check.sh"

rlJournalStart
    rlPhaseStartSetup "Verify Hardware & Setup"
        hwVerify    # Must be the FIRST line in Test Phase; exits 0 if not met
        # ... package install, temp dir creation ...
    rlPhaseEnd

    rlPhaseStartTest "Multi-server Failover Test"
        hwRunOnServer 1 "systemctl start my_service"
        hwRunOnServer 2 "systemctl start my_service"
        # ... test logic ...
    rlPhaseEnd

    rlPhaseStartCleanup "Cleanup"
        # ... cleanup ...
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
```

---

## 6. Naming Conventions

### Test Case Directory Naming

Format: `test_{pkg}_{feature_description}`

- All lowercase, underscore-separated
- Feature description in English with underscores
- Examples: `test_acl_getfacl_basic`, `test_bash_variable_expansion`, `test_coreutils_ls_long_format`

### Test Case Summary

Format in `main.fmf`:

```yaml
summary: Test Type - Package - Feature Description
```

Examples:
- `Functional Test - acl - getfacl basic functionality`
- `Smoke Test - network - ping basic connectivity`

### Script File Naming

Always `test.sh`, placed in the test case directory. Not named after the feature.

---

## 7. Verification Checklist

Before submitting a test case, verify all of the following:

- [ ] `test.sh` has correct shebang: `#!/bin/bash`
- [ ] Sources beakerlib: `. /usr/share/beakerlib/beakerlib.sh || exit 1`
- [ ] Three-phase structure: Setup → Test → Cleanup
- [ ] `TmpDir=$(mktemp -d)` in Setup, cleaned in Cleanup
- [ ] Shared library included if using lib.sh: `. "$(dirname "$0")/../lib.sh"`
- [ ] Package setup function called in Setup phase (e.g. `aclSetup`)
- [ ] `main.fmf` has `summary`, `test`, `tag`, `duration`, `tier`, `path`, `require`
- [ ] `tag` includes the correct test type (e.g. `functional`)
- [ ] `rlRun` exit code parameters are correct (0 for success, 1 for expected failure)

---

## 8. Unit Tests (Code Quality Checks)

The `unittests/` directory contains unit tests for the test framework itself, ensuring all test cases comply with project conventions. Run these locally before submitting a pull request.

### 8.1 Running Unit Tests

```bash
# Run all unit tests
python -m unittest discover -s unittests -p "test_*.py" -v

# Run a single test file
python -m unittest unittests.test_tests_quality -v
```

### 8.2 Test Case Overview

All tests are in `unittests/test_tests_quality.py`, currently **10 tests** across 5 categories:

| Category | Test | Description |
|----------|------|-------------|
| **Chinese Characters** | `test_no_chinese_in_tests` | Ensures no Chinese characters exist in `tests/` directory files |
| **Mojibake** | `test_no_mojibake_in_tests` | Detects Latin-1 mojibake (e.g. `ä½ å¥½`) in `tests/` directory files |
| **Shell Script Compliance** | `test_test_sh_compliance` | Validates `test.sh` files follow BeakerLib structure (`rlJournalStart`, `rlPhaseStart*`, `rlJournalEnd`, `#!/bin/bash`) |
| | `test_lib_sh_compliance` | Validates `lib.sh` files follow shared library conventions (`library-prefix` annotation, `*Setup()` function) |
| | `test_no_crlf_in_sh_files` | Ensures all `.sh` files use LF line endings, not CRLF |
| | `test_main_fmf_yaml_valid` | Validates `main.fmf` files are valid YAML with required fields (`summary`, `test`, `tag`, `duration`, `tier`, `path`, `require`) |
| **Executable Permissions** | `test_sh_files_executable_in_git` | Ensures `.sh` files have executable (`100755`) permission in git |
| | `test_no_non_sh_executable_in_tests` | Ensures no non-`.sh` files have executable permission in `tests/` |
| **Indentation** | `test_no_tab_in_sh` | Ensures no tab characters in `.sh` files |
| | `test_sh_indentation_multiple_of_4` | Ensures indentation uses multiples of 4 spaces (4 per nesting level) |

### 8.3 Key Design Notes

- **Git-based checks**: Most tests read committed content via `git show` to avoid CRLF conversion interference from `core.autocrlf=true`.
- **Heredoc awareness**: The indentation test excludes heredoc body content (`<<WORD ... WORD`) to avoid false positives from embedded code (C, Makefile, etc.).
- **All 10 tests must pass** before submitting a PR.

---

## 9. FAQ

### Q: Error `beakerlib.sh: No such file or directory`

```bash
sudo dnf install -y beakerlib
```

### Q: tmt command not found

```bash
# dnf install
sudo dnf install -y tmt

# Or pip install (riscv64)
sudo pip3 install --break-system-packages tmt
```

### Q: Tests fail due to insufficient permissions

Some test scripts use `sudo` for privileged operations; ensure the current user has sudo access:

```bash
# Verify sudo works
sudo whoami
```

### Q: How to see which tests a plan includes (without executing)?

```bash
tmt plan show /plans/functional
tmt test ls /tests/functional/pkgs/acl
```

### Q: View detailed results of the last run

```bash
tmt run --last report -fvvv
```

> **Note**: `tmt run --last report` can sometimes be slow due to tmt internally polling historical data. If you just want a summary, read `run.yaml` directly or check each case's `output.txt`.

### Q: Error `Synchronization lock ... is stale` when running tmt

```bash
# Clean up stale tmt lock files (usually left by root-owned runs)
sudo rm -f /var/tmp/tmt-test.pid.lock
```

---

## 10. Practical Example: ACL Test Suite

This section uses the `acl` test suite as a complete walkthrough from environment setup to viewing results.

### 10.1 Prerequisites

- A clean openRuyi server (this example: 10.20.237.192:12055)
- git, tmt, beakerlib installed (see Section 1)

### 10.2 Clone Repository and Install Dependencies

```bash
git clone https://git.openruyi.cn/woqidaideshi/openruyi-autotest.git
cd openruyi-autotest

# Install tmt and test dependencies
sudo dnf install -y tmt beakerlib python-six
sudo dnf install -y acl         # ACL test target package
```

### 10.3 (Optional) Configure topology.env

```bash
cp topology.env.example topology.env
vim topology.env
```

Write:

```ini
TEST_SERVER_COUNT=1
TEST_SERVER_1_HOST=10.20.237.192
TEST_SERVER_1_PORT=12055
TEST_SERVER_1_USER=openruyi
TEST_SERVER_1_PASSWORD=openruyi
```

> If the current user is already `openruyi` and running locally, you can skip configuring `topology.env`; tmt will auto-detect.

### 10.4 Clean Up Lock Files (Important)

If tmt was previously run but interrupted abnormally, lock files may remain:

```bash
sudo rm -f /var/tmp/tmt-test.pid.lock
```

### 10.5 Execute ACL Test Suite

```bash
cd ~/openruyi-autotest

tmt run --all plan --name /plans/functional \
    test --name /tests/functional/pkgs/acl \
    provision --feeling-safe
```

**Command breakdown:**

| Parameter | Meaning |
|-----------|---------|
| `--all` | Skip interactive confirmation (use with `--feeling-safe`) |
| `plan --name /plans/functional` | Use the functional test plan (defined in `plans/functional.fmf`) |
| `test --name /tests/functional/pkgs/acl` | Only run cases under `tests/functional/pkgs/acl/` |
| `provision --feeling-safe` | Local execution, skip confirmation |

**Expected output key lines:**

```
Found 1 plan.
summary: Functional Test - Verify all functional test cases
discover
    how: fmf
    directory: /home/openruyi/openruyi-autotest/tests/functional/pkgs/acl
    filter: tag:functional
    tests:
        /tests/functional/pkgs/acl/test_acl_acl_inheritance
        /tests/functional/pkgs/acl/test_acl_acl_permission_verify
        ...
```

### 10.6 View Results

```bash
# Enter the most recent run directory
cd $(ls -dt /var/tmp/tmt/run-* | head -1)

# View results for a specific case
cat plans/functional/execute/data/guest/default-0/tests/functional/pkgs/acl/test_acl_getfacl_basic-1/output.txt
```

**Expected result**: All cases show `PASS` at the end of the output.

### 10.7 FAQ

**Q: `acl` package not found?**

```bash
sudo dnf install -y acl
```

**Q: Which cases are available under the acl suite?**

```bash
tmt test ls /tests/functional/pkgs/acl
```
