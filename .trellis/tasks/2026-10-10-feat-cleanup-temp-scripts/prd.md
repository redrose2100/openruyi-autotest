# chore: remove temporary scripts and data files from repo root

## Goal

Remove 18 temporary one-off scripts and data files from repository root. These were created during Round4 CI fixes (fe102b98a) and test-split work (68f97cfde) and have all served their purpose. Generated tests already live under `tests/functional/pkgs/`, and code fixes have been applied. None of these files are referenced by any other file in the repo.

## Requirements

### R1: Remove one-off Python analysis/fix scripts
Delete 14 `.py` files used for one-time diagnosis and batch fixes:
`_analyze_fails.py`, `_check_gcc.py`, `_check_tests.py`, `_fix_error_pattern.py`, `_fix_version_help.py`, `coverage_analyzer.py`, `coverage_analyzer_v2.py`, `fix_and_cleanup_coreutils.py`, `gen_curl_tests.py`, `gen_p0_tests.py`, `gen_p1_tests.py`, `gen_p3_tests.py`, `gen_p3b_tests.py`, `split_coreutils_tests.py`

### R2: Remove one-off PowerShell analysis scripts
Delete `analyze_libs.ps1` and `analyze_pkgs.ps1`.

### R3: Remove one-off data files
Delete `ci_log_round4.txt` and `pkg_list.txt`.

### R4: Ensure no references remain
Verify no other file in the repo imports or references any of the deleted files.

## Test Points

- TP1: All 18 files are removed from the working tree
- TP2: `git status` confirms 18 deletions staged for commit
- TP3: Repo grep confirms no remaining references to deleted file names outside `.venv/`
- TP4: `tests/functional/pkgs/` tests remain intact (generated output unaffected)

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
