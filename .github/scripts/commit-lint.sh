#!/usr/bin/env bash
# Check that all commit messages in the given range follow the project's
# commit guide (docs/commit_guide.md, Conventional Commits based):
#
#   <type>(<scope>): <summary>
#
# Usage: commit-lint.sh [<git-range>]
#   If <git-range> is omitted, all commits reachable from HEAD are checked.
set -euo pipefail

GUIDE_URL="https://github.com/woqidaideshi/openruyi-autotest/blob/main/docs/commit_guide.md"

RANGE="${1:-}"
if [ -z "$RANGE" ]; then
  RANGE="HEAD"
fi

# Allowed types from docs/commit_guide.md
TYPES="feat|fix|docs|style|refactor|perf|test|chore|ci|build"

status=0
total=0
checked=0

while IFS= read -r subject; do
  total=$((total + 1))
  # Skip merge and revert commits whose messages are auto-generated.
  case "$subject" in
    Merge*|Revert*) continue ;;
  esac
  checked=$((checked + 1))

  # 1. Basic format: <type>(<scope>): <summary>
  if ! printf '%s\n' "$subject" | grep -qE "^($TYPES)(\([a-z0-9._/-]+\))?(!)?: .+"; then
    echo "::error::Invalid commit message format: \"$subject\""
    echo "::error::Expected: <type>(<scope>): <summary>  (see $GUIDE_URL)"
    status=1
    continue
  fi

  # 2. Plain ASCII English summary (no Chinese / non-ASCII chars)
  if ! printf '%s\n' "$subject" | grep -qE '^[ -~]+$'; then
    echo "::error::Commit summary must be plain ASCII English: \"$subject\""
    status=1
    continue
  fi

  # 3. Summary starts with a lowercase letter
  summary=$(printf '%s\n' "$subject" | sed -E 's/^[A-Za-z]+(\([^)]*\))?(!)?: //')
  if ! printf '%s\n' "$summary" | grep -qE '^[a-z]'; then
    echo "::error::Commit summary must start with a lowercase letter: \"$subject\""
    status=1
    continue
  fi

  # 4. Summary must not exceed 72 characters
  if [ ${#subject} -gt 72 ]; then
    echo "::error::Commit summary exceeds 72 characters (${#subject}): \"$subject\""
    status=1
    continue
  fi

  # 5. No trailing period
  if printf '%s\n' "$subject" | grep -qE '\.$'; then
    echo "::error::Commit summary must not end with a period: \"$subject\""
    status=1
    continue
  fi
done < <(git log --format=%s "$RANGE")

echo "Checked $checked commit(s) (skipped $((total - checked)) merge/revert) in range: $RANGE"
if [ "$status" -ne 0 ]; then
  echo ""
  echo "============================================================"
  echo "COMMIT MESSAGE(S) DO NOT FOLLOW THE PROJECT STANDARDS."
  echo "Please read the commit guide:"
  echo "  $GUIDE_URL"
  echo "============================================================"
  exit 1
fi
echo "OK: all commit messages follow the guide: $GUIDE_URL"
