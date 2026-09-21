# Commit & MR Standards

> Commit message and Merge Request standards for the openruyi-autotest project.
> Follows the [Conventional Commits](https://www.conventionalcommits.org/) industry standard.

---

## 1. Commit Message Standards

### 1.1 Basic Format

```
<type>(<scope>): <short summary>

<optional body>

<optional footer>
```

- **type**: Commit type (required)
- **scope**: Affected area (optional, recommended)
- **short summary**: Brief description, max 72 chars, lowercase English, no trailing period
- **body**: Detailed explanation (optional), separated from summary by a blank line
- **footer**: Footnotes (optional), e.g. `BREAKING CHANGE:` or related issue

### 1.2 Type Values

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add default extra-hardware-require to all test suites` |
| `fix` | Bug fix | `fix: hw_check.sh awk pattern to match indented YAML keys` |
| `docs` | Documentation changes | `docs: enhance development guide with ACL walkthrough` |
| `style` | Code formatting (no logic change) | `style: fix shellcheck warnings in lib.sh` |
| `refactor` | Refactoring (not feat or fix) | `refactor: move config resolution into main()` |
| `perf` | Performance optimization | `perf: cache dnf metadata in test setup` |
| `test` | Test case changes | `test: add getfacl error handling test cases` |
| `chore` | Build/tool/dependency changes | `chore: remove qemu_daemon.py` |
| `ci` | CI/CD changes | `ci: add shellcheck to pre-commit hooks` |
| `build` | Build system changes | `build: update tmt to 1.75.0` |

### 1.3 Scope (Optional)

Use the affected module or directory name:

| Scope | Meaning |
|-------|---------|
| `acl` | ACL test suite |
| `kernel` | Kernel tests |
| `hw_check` | Hardware check library |
| `ltp` | LTP test suite |
| `plan` | Test plans |
| `tmt` | tmt framework config |
| _(omitted)_ | Use when scope is unclear or cross-module |

### 1.4 Examples

```bash
# Basic format
feat(acl): add chacl command test suite

# With body
fix(kernel): resolve sched_attr redefinition in LTP 20260529

The sched_attr struct was redefined in the 20260529 tag. Use
range-based sed to patch only the conflicting definition without
affecting other uses of the struct.

# Breaking change
feat(config)!: switch from YAML to TOML for topology config

BREAKING CHANGE: topology.env is now topology.toml.
All existing topology.env files must be migrated.
```

### 1.5 Notes

- **Use plain ASCII English for summary** (Gitea does not support Chinese commit messages)
- Summary must not exceed 72 characters
- Use imperative mood: `add` not `added`, `fix` not `fixed`
- Each commit does one thing; avoid mixing unrelated changes
- Check the staging area with `git diff --cached` before committing

---

## 2. Merge Request Standards

### 2.1 MR Title

Follow the same Conventional Commits format as commits:

```
<type>(<scope>): <short summary>
```

Examples:

```
docs: enhance development guide - extra-hardware-require, test discovery, ACL walkthrough
feat(ltp): add 65 functional test suites with kirk runner
fix(hw_check): correct awk field parsing for indented YAML
```

### 2.2 MR Description Template

```markdown
## Summary

Briefly describe what this MR does and why.

## Changes

- Change 1: description
- Change 2: description
- Change 3: description

## Verification

- [ ] Local bash test.sh passes
- [ ] tmt run passes for affected tests
- [ ] No regressions in existing tests

## Related Issues

Closes #123
Refs: #456
```

### 2.3 MR Description Example

```markdown
## Summary

This PR comprehensively enhances `docs/development-guide.md` (+448/-36 lines),
covering structural additions, environment constraints documentation,
verification checklist expansion, and an ACL development walkthrough.

## Changes

- Section 3.3.1: New test discovery mechanism diagram
- Section 3.4: lib.sh design patterns with reference counting
- Section 4: FMF field table now includes framework, extra-hardware-require, environment
- Section 5.6: hwVerify placement documented (must be first line in Test Phase)
- Section 7: Verification checklist expanded from 5 to 8 items
- Section 8: FAQ expanded from 3 to 6 questions
- Section 9: Complete ACL development walkthrough with 3 full examples

## Verification

- [x] All examples syntax-checked with bash -n
- [x] tmt test ls confirms all referenced tests are discoverable
- [x] Document renders correctly in VS Code Markdown preview
```

### 2.4 Notes

- **MR titles and descriptions must use plain English** (Gitea does not support Chinese characters; they render as mojibake `?`)
- Avoid backtick-wrapped Markdown code in MR descriptions (Gitea rendering may be abnormal); use plain text when necessary
- One MR focuses on one topic; avoid mixing multiple independent changes
- Ensure all CI checks pass before merging
- Recommended merge method: **Rebase and Merge** (keeps commit history linear)

---

## 3. Branch Naming Standards

| Branch | Purpose |
|--------|---------|
| `main` | Stable version, only accepts MR merges |
| `dev` | Development mainline, daily commit target |
| `feat/<name>` | Feature branch (optional, for large features) |
| `fix/<name>` | Fix branch (optional, for urgent fixes) |

Daily development workflow:

```
git checkout dev
# ... code ...
git add <files>
git commit -m "feat(scope): description"
git push origin dev
# Then create an MR from dev → main on Gitea
```

---

## 4. Related Documents

- [Development Guide](development-guide.md) — Complete test case development workflow
- [User Guide](user_guide.md) — Test execution and usage instructions
- [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/)

---

## 5. Practical Walkthrough: ACL Test Suite

The following uses the `tests/functional/pkgs/acl/` test suite to demonstrate complete Commit and MR formats for adding, modifying, fixing, and refactoring.

ACL test suite structure:

```
tests/functional/pkgs/acl/
├── main.fmf                     # Suite-level metadata
├── lib.sh                       # Shared library (reference-count install/uninstall)
├── test_acl_getfacl_basic/      # getfacl basic functionality (7 options)
├── test_acl_setfacl_basic/      # setfacl CRUD operations
├── test_acl_setfacl_advanced/   # default ACL, --set, -M
├── test_acl_setfacl_recursive/  # -R recursive set
├── test_acl_setfacl_remove/     # -x/-X batch remove
├── test_acl_setfacl_symlink/    # -L/-P symlink handling
├── test_acl_chacl_command/      # chacl command
├── test_acl_acl_inheritance/    # Default ACL inheritance
├── test_acl_acl_permission_verify/  # ACL permission enforcement verification
├── test_acl_error_handling/     # Error paths (nonexistent file/user, invalid permissions)
└── test_acl_special_cases/      # Multi-user/group, --test dry-run, backup/restore
```

### 5.1 Scenario 1: Add a New Test Case

**Scenario**: Add `getfacl` basic functionality test to the ACL suite, covering 7 CLI options.

**Files involved**:

| Operation | File |
|-----------|------|
| New | `tests/functional/pkgs/acl/test_acl_getfacl_basic/main.fmf` |
| New | `tests/functional/pkgs/acl/test_acl_getfacl_basic/test.sh` |

**Commit**:

```bash
git add tests/functional/pkgs/acl/test_acl_getfacl_basic/
git commit -m "feat(acl): add getfacl basic test covering 7 CLI options"
```

**Commit breakdown**:

| Element | Value | Explanation |
|---------|-------|-------------|
| type | `feat` | New feature (new test case = new feature) |
| scope | `acl` | Affects ACL test suite |
| summary | `add getfacl basic test covering 7 CLI options` | 47 chars, imperative, describes coverage |

### 5.2 Scenario 2: Modify/Update Existing Tests

**Scenario**: Add two new error paths to `test_acl_error_handling`: `setfacl` with invalid mask value, `getfacl` on a file without permissions.

**Files involved**:

| Operation | File |
|-----------|------|
| Modify | `tests/functional/pkgs/acl/test_acl_error_handling/test.sh` |

**Commit**:

```bash
git add tests/functional/pkgs/acl/test_acl_error_handling/test.sh
git commit -m "feat(acl): add invalid mask and permission-denied error cases"
```

**Commit breakdown**:

| Element | Value | Explanation |
|---------|-------|-------------|
| type | `feat` | Added new capability (expanded error path coverage) |
| scope | `acl` | Affects ACL test suite |

> **Note**: If only changing test descriptions, comments, or formatting, use `style` or `refactor` instead of `feat`.

### 5.3 Scenario 3: Bug Fix

**Scenario**: Found that `rlRun "! getfacl ... | grep ..."` in `test_acl_setfacl_basic` has incorrect exit code logic — the `!` negation does not work as expected inside `rlRun`, causing false PASS.

**Files involved**:

| Operation | File |
|-----------|------|
| Modify | `tests/functional/pkgs/acl/test_acl_setfacl_basic/test.sh` |

**Commit**:

```bash
git add tests/functional/pkgs/acl/test_acl_setfacl_basic/test.sh
git commit -m "fix(acl): correct exit code check in setfacl_basic negative tests"
```

**Commit breakdown**:

| Element | Value | Explanation |
|---------|-------|-------------|
| type | `fix` | Bug fix |
| scope | `acl` | Affects ACL test suite |

### 5.4 Scenario 4: Refactoring

**Scenario**: Split the ACL test suite from a single large script into 11 independent per-case directories, each with its own `main.fmf` and `test.sh`. Also extract shared install/uninstall logic into `lib.sh`.

**Files involved**:

| Operation | Count | Description |
|-----------|-------|-------------|
| Delete | ~5 | Old `setup.sh`, `teardown.sh`, `test.sh` |
| New | 12 | `lib.sh` + 11 `test_acl_*/main.fmf` |
| Modify | 12 | 11 `test_acl_*/test.sh` + `main.fmf` |

**Commit**:

```bash
git add tests/functional/pkgs/acl/
git commit -m "refactor(acl): split into per-case dirs with shared lib.sh"
```

**Commit breakdown**:

| Element | Value | Explanation |
|---------|-------|-------------|
| type | `refactor` | Refactoring, no test logic changed |
| scope | `acl` | Affects ACL test suite |

### 5.5 Scenario 5: Documentation Update

**Scenario**: Add ACL development walkthrough examples to the development guide.

**Commit**:

```bash
git add docs/development-guide.md
git commit -m "docs: add ACL development walkthrough to developer guide"
```

**Commit breakdown**:

| Element | Value | Explanation |
|---------|-------|-------------|
| type | `docs` | Documentation change |
| scope | _(omitted)_ | Cross-module documentation, no scope needed |

---

### 5.6 Scenario 6: Complete ACL Suite MR

Combining the 5 commits above into a single `dev → main` MR:

**MR Title**:

```
feat(acl): add getfacl and error-handling tests, fix exit code bug, refactor to per-case dirs
```

**MR Description**:

```markdown
## Summary

This MR enhances the ACL test suite with new test cases, bug fixes,
and a structural refactoring for better maintainability.

Related commits in this MR:
- feat(acl): add getfacl basic test covering 7 CLI options
- feat(acl): add invalid mask and permission-denied error cases
- fix(acl): correct exit code check in setfacl_basic negative tests
- refactor(acl): split into per-case dirs with shared lib.sh
- docs: add ACL development walkthrough to developer guide

## Changes

### New Tests
- getfacl basic: covers -a, -d, -c, -n, -t options (7 features)
- error handling: added invalid mask and permission-denied edge cases

### Bug Fixes
- Fixed rlRun exit code logic in setfacl_basic negative tests
  (the ! negation operator does not work inside rlRun)

### Refactoring
- Split monolithic ACL test into 11 independent per-case directories
- Extracted shared package install/uninstall into lib.sh
- Each test case now has its own main.fmf with granular duration/tier

### Documentation
- Added Section 9 to development-guide.md with ACL walkthrough

## Verification

- [x] All 11 ACL test cases pass: tmt run plan --name /plans/functional test --name /tests/functional/pkgs/acl
- [x] Each case runs independently without side effects
- [x] lib.sh reference counting works correctly (acl installed once, uninstalled once)
- [x] No regressions in other functional test suites
- [x] getfacl basic covers all 7 CLI options
- [x] Error cases correctly report FAIL for invalid input
```

**MR breakdown**:

| Element | Explanation |
|---------|-------------|
| Title | Summarizes MR topic, comma-separated subtopics |
| Summary | One-sentence overview + list of related commits |
| Changes | Grouped by category (New / Fix / Refactor / Docs), each item concrete |
| Verification | Lists verification steps and results, each check specific and reproducible |
