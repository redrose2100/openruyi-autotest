# -*- coding: utf-8 -*-
"""
post-pr-comment 命令

流水线步骤 5：将测试结果汇总发布为 PR 评论。

输入：test_results.json
输出：PR 评论（GitHub API）

依赖环境变量：
  GITHUB_TOKEN        # github.token
  GITHUB_REPOSITORY   # owner/repo
  PR_NUMBER           # PR 编号
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
    """生成 PR 评论 Markdown"""
    summary = results.get("summary", {})
    ok = results.get("ok", False)

    lines = []
    lines.append("## 🤖 自动测试验证报告")
    lines.append("")
    lines.append(f"**结果**: {'✅ 全部通过' if ok else '❌ 存在失败'}  \n")
    lines.append(
        f"**汇总**: 通过 `{summary.get('pass', 0)}` / 失败 `{summary.get('fail', 0)}`"
        f" / 错误 `{summary.get('error', 0)}` / 跳过 `{summary.get('skip', 0)}`"
        f" / 总计 `{summary.get('total', 0)}`"
    )
    lines.append("")
    lines.append("### 详细结果")
    lines.append("")
    lines.append("| 状态 | 测试路径 | Host:Port |")
    lines.append("|------|----------|-----------|")
    for r in results.get("results", []):
        status = r.get("status", "?")
        icon = {"pass": "✅", "fail": "❌", "error": "⚠️", "skip": "⏭️"}.get(status, "❓")
        lines.append(
            f"| {icon} {status} | `{r.get('test_path', '')}` | "
            f"{r.get('host_ip', '')}:{r.get('qemu_port', '')} |"
        )
    lines.append("")

    # 附上失败详情（最多 3 个，截断）
    fails = [r for r in results.get("results", []) if r.get("status") in ("fail", "error")]
    if fails:
        lines.append("### 失败详情")
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
    """将测试结果发布为 PR 评论"""

    name = "post-pr-comment"
    description = "将 test_results.json 汇总为 GitHub PR 评论"

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
