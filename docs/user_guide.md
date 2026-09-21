# User Guide

> For **clean server** environments, getting started from scratch.

---

## 1. Environment Setup

### 1.1 Install git

```bash
sudo dnf install -y git
```

### 1.2 Clone the Repository

```bash
git clone https://git.openruyi.cn/woqidaideshi/openruyi-autotest.git
cd openruyi-autotest
```

### 1.3 Install tmt and beakerlib

Test cases are managed and executed using the tmt (Test Management Tool) framework:

```bash
# Install tmt (basic version, supports local execution)
sudo dnf install -y tmt

# Install beakerlib test framework
sudo dnf install -y beakerlib

# beakerlib runtime dependencies
sudo dnf install -y python-six

# Verify installation
tmt --version
rpm -q beakerlib
```

> **riscv64 architecture**: `tmt` may not be in the dnf repo; install via pip:
> ```bash
> sudo dnf install -y python3 python3-pip rust gcc gcc-c++ beakerlib
> sudo pip3 install --break-system-packages tmt
> ```

### 1.4 Configure Test Topology (Optional)

Test plans automatically detect whether the current machine's hardware (CPU/memory/disk/NICs) meets test case hardware requirements. To run tests across multiple servers, or customize server connection info, configure `topology.env`:

```bash
# Copy template
cp topology.env.example topology.env

# Modify for your environment
vim topology.env
```

**Configuration variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `TEST_SERVER_COUNT` | Number of available servers | 1 |
| `TEST_SERVER_1_HOST` | Server 1 IP/hostname | (none) |
| `TEST_SERVER_1_PORT` | Server 1 SSH port | 22 |
| `TEST_SERVER_1_USER` | Server 1 login username | root |
| `TEST_SERVER_1_PASSWORD` | Server 1 login password | (none) |

Multi-server example (3 servers):

```ini
TEST_SERVER_COUNT=3

TEST_SERVER_1_HOST=192.168.1.10
TEST_SERVER_1_PORT=22
TEST_SERVER_1_USER=root
TEST_SERVER_1_PASSWORD=mypassword

TEST_SERVER_2_HOST=192.168.1.11
TEST_SERVER_2_PORT=12055
TEST_SERVER_2_USER=openruyi
TEST_SERVER_2_PASSWORD=mypassword

TEST_SERVER_3_HOST=192.168.1.12
TEST_SERVER_3_USER=root
# Port/password use defaults (22 / no password) when not set
```

> **Not configuring `topology.env` does not affect single-machine testing**. The system treats the current machine as the only server (`TEST_SERVER_COUNT` defaults to 1), and hardware resources are auto-detected via system commands.

---

## 2. Running a Single Test Case

Example: `test_acl_getfacl_basic` in the acl test suite:

```bash
cd openruyi-autotest

tmt run --all --verbose plan --name /plans/functional \
    test --name /tests/functional/pkgs/acl/test_acl_getfacl_basic \
    provision --feeling-safe
```

> **About `--feeling-safe`**: tmt asks for user confirmation before execution by default; this flag skips interactive confirmation, suitable for automation/unattended scenarios.

---

## 3. Running a Single Test Suite

Example: acl:

```bash
cd openruyi-autotest

tmt run --all plan --name /plans/functional \
    test --name /tests/functional/pkgs/acl \
    provision --feeling-safe
```

---

## 4. Running All Cases of a Test Type

Example: functional tests, covering 202 packages with 566 test cases:

```bash
cd openruyi-autotest

tmt run --all plan --name /plans/functional \
    provision --feeling-safe
```

Example: feature tests:

```bash
tmt run --all plan --name /plans/feature \
    provision --feeling-safe
```

---

## 5. Viewing Test Results and Logs

### 5.1 tmt Results Directory

Each tmt run creates a run directory under `/var/tmp/tmt/run-*` containing detailed logs for all test cases:

```bash
# List all historical runs
ls -lt /var/tmp/tmt/

# Enter the most recent run directory
cd $(ls -dt /var/tmp/tmt/run-* | head -1)
```

Run directory structure:

```
/var/tmp/tmt/run-XXX/
├── plans/
│   └── {plan-name}/            # e.g. functional
│       └── execute/
│           └── data/
│               └── guest/      # local execution shows as guest
│                   └── default-0/
│                       └── tests/functional/pkgs/acl/
│                           ├── test_acl_getfacl_basic-1/
│                           │   └── output.txt    # Full output of this case
│                           ├── test_acl_setfacl_basic-2/
│                           │   └── output.txt
│                           └── ...
└── run.yaml                    # Run metadata
```

### 5.2 Viewing a Single Case Log

```bash
# Enter the most recent run directory
RUN_DIR=$(ls -dt /var/tmp/tmt/run-* | head -1)

# Path includes plans/ and guest/default-0/ levels
BASE="$RUN_DIR/plans/functional/execute/data/guest/default-0"

# View full output of a specific test case
cat "$BASE/tests/functional/pkgs/acl/test_acl_getfacl_basic-1/output.txt"
```

### 5.3 Viewing Summary Report

```bash
# Brief report
tmt run --last report

# Detailed report (with stdout/stderr for each case)
tmt run --last report -fvvv
```

### 5.4 Viewing Execution Status of All Cases

```bash
RUN_DIR=$(ls -dt /var/tmp/tmt/run-* | head -1)
BASE="$RUN_DIR/plans/functional/execute/data/guest/default-0"

# List all output.txt files and show last few lines (usually contains PASS/FAIL)
find "$BASE" -name "output.txt" | sort | while read f; do
    dir=$(dirname "$f")
    echo "=== $(basename "$dir") ==="
    tail -5 "$f"
    echo ""
done
```

---

## 6. Running All Tests

Run all tests (all plans) from the project root:

```bash
cd openruyi-autotest

tmt run --all provision --how local --feeling-safe
```

---

## 7. Directory Structure Quick Reference

```
tests/
├── smoke/             # Smoke tests (100 cases)
│   ├── archive/       # Archive tools (tar, gzip, xz)
│   ├── dev_tools/     # Development tools
│   ├── disk_fs/       # Disk/filesystem
│   ├── filesystem/    # Filesystem operations
│   ├── kernel/        # Kernel functions
│   ├── logging/       # Logging system
│   ├── network/       # Network tools
│   ├── package_mgmt/  # Package management
│   ├── permissions/   # Permission management
│   ├── process/       # Process management
│   ├── scripting/     # Scripting languages
│   ├── security/      # Security-related
│   ├── service_mgmt/  # Service management
│   ├── shell_basics/  # Shell basics
│   ├── system_info/   # System information
│   ├── text_processing/# Text processing
│   └── user_mgmt/     # User management
├── functional/pkgs/   # Functional tests (202 packages, 566 cases)
│   ├── acl/           # ACL permission management (reference standard)
│   ├── attr/          # Extended attributes
│   ├── bash/          # Bash shell
│   ├── coreutils/     # Core utilities
│   ├── ...            # More packages
├── security/          # Security tests (106 cases)
│   ├── cve/           # CVE vulnerability verification
│   └── nmap/          # Nmap port scanning
├── compatibility/     # Compatibility tests (188 cases)
│   └── ltp_posix/     # LTP POSIX interface compatibility
├── performance/       # Performance tests
│   └── unixbench/     # UnixBench benchmarks
├── feature/           # Feature tests
│   └── <xxx>/         # Feature name
└── reliability/       # Reliability tests
    └── test.sh
```

---

## 8. FAQ

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

## 9. Practical Example: ACL Test Suite

This section uses the `acl` test suite as a complete walkthrough from environment setup to viewing results.

### 9.1 Prerequisites

- A clean openRuyi server (this example: 10.20.237.192:12055)
- git, tmt, beakerlib installed (see Section 1)

### 9.2 Clone Repository and Install Dependencies

```bash
git clone https://git.openruyi.cn/woqidaideshi/openruyi-autotest.git
cd openruyi-autotest

# Install tmt and test dependencies
sudo dnf install -y tmt beakerlib python-six
sudo dnf install -y acl         # ACL test target package
```

### 9.3 (Optional) Configure topology.env

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

### 9.4 Clean Up Lock Files (Important)

If tmt was previously run but interrupted abnormally, lock files may remain:

```bash
sudo rm -f /var/tmp/tmt-test.pid.lock
```

### 9.5 Execute ACL Test Suite

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

### 9.6 View Results

```bash
# Enter the most recent run directory
cd $(ls -dt /var/tmp/tmt/run-* | head -1)

# View results for a specific case
cat plans/functional/execute/data/guest/default-0/tests/functional/pkgs/acl/test_acl_getfacl_basic-1/output.txt
```

**Expected result**: All cases show `PASS` at the end of the output.

### 9.7 FAQ

**Q: `acl` package not found?**

```bash
sudo dnf install -y acl
```

**Q: Which cases are available under the acl suite?**

```bash
tmt test ls /tests/functional/pkgs/acl
```
