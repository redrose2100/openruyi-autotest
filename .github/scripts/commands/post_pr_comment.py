# -*- coding: utf-8 -*-
"""
post-pr-comment command

Pipeline step 5: Aggregate test results and publish as a PR comment.

Input: test_results.json
Output: PR comment (GitHub API)

Required environment variables:
  GITHUB_TOKEN        # github.token
  GITHUB_REPOSITORY   # owner/repo
  PR_NUMBER           # PR number
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Dict

from core.base import BaseCommand
from core.github import GitHubClient

logger = logging.getLogger("ci_cli.commands.post_pr_comment")


def build_comment(results: dict) -> str:
    """Generate PR comment Markdown"""
    summary = results.get("summary", {})
    ok = results.get("ok", False)

    lines = []
    lines.append("## 🤖 Automated Test Verification Report")
    lines.append("")
    lines.append(f"**Result**: {'✅ All Passed' if ok else '❌ Has Failures'}  \n")
    lines.append(
        f"**Summary**: Passed `{summary.get('pass', 0)}` / Failed `{summary.get('fail', 0)}`"
        f" / Error `{summary.get('error', 0)}` / Skipped `{summary.get('skip', 0)}`"
        f" / Total `{summary.get('total', 0)}`"
    )
    lines.append("")
    lines.append("### Detailed Results")
    lines.append("")
    lines.append("| Status | Test Path | Host:Port |")
    lines.append("|------|----------|-----------|")
    for r in results.get("results", []):
        status = r.get("status", "?")
        icon = {"pass": "✅", "fail": "❌", "error": "⚠️", "skip": "⏭️"}.get(status, "❓")
        lines.append(
            f"| {icon} {status} | `{r.get('test_path', '')}` | "
            f"{r.get('host_ip', '')}:{r.get('qemu_port', '')} |"
        )
    lines.append("")

    # Include failure details (max 3, truncated)
    fails = [r for r in results.get("results", []) if r.get("status") in ("fail", "error")]
    if fails:
        lines.append("### Failure Details")
        lines.append("")
        for r in fails[:3]:
            lines.append(f"**{r.get('test_path', '')}**")
            out = (r.get("output") or "")[-1500:]
            lines.append("```text")
            lines.append(out)
            lines.append("```")
            lines.append("")
    return "\n".join(lines)


class PostPrCommentCommand(BaseCommand):
    """Publish test results as a PR comment"""

    name = "post-pr-comment"
    description = "Aggregate test_results.json into a GitHub PR comment"

    def setup_parser(self, parser):
        parser.add_argument("--results", default="test_results.json",
                            help="Path to test_results.json (default: test_results.json)")

    def run(self, args) -> int:
        results_path = Path(args.results)
        client = GitHubClient()
        if not client.configured:
            self.log_error("Missing GITHUB_TOKEN / GITHUB_REPOSITORY / PR_NUMBER")
            return 1

        if not results_path.exists():
            self.log_error(f"Results file not found: {results_path}, skip comment")
            return 1

        with open(results_path, encoding="utf-8") as f:
            results = json.load(f)

        comment = build_comment(results)
        html_url = client.post_pr_comment(comment)
        if html_url:
            self.log_info(f"Comment posted: {html_url}")
            return 0
        self.log_error("Failed to post comment")
        return 1
