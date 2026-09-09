#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post_pr_comment.py

流水线步骤 5：将测试结果汇总发布为 PR 评论。

输入：test_results.json
输出：PR 评论（GitHub API）

依赖环境变量：
  GITHUB_TOKEN        # github.token
  GITHUB_REPOSITORY   # owner/repo
  PR_NUMBER           # PR 编号
"""

import json
import os
import sys
import urllib.request
import urllib.error


def api_request(method: str, url: str, body: dict = None, token: str = "") -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        print(f"API error {e.code} for {method} {url}: {e.read().decode('utf-8', 'replace')[:500]}")
        return {}
    except Exception as e:
        print(f"API request failed: {e}")
        return {}


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


def main() -> int:
    results_path = sys.argv[1] if len(sys.argv) > 1 else "test_results.json"
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    if not token or not repo or not pr_number:
        print("Missing GITHUB_TOKEN / GITHUB_REPOSITORY / PR_NUMBER")
        return 1

    with open(results_path, encoding="utf-8") as f:
        results = json.load(f)

    comment = build_comment(results)
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    resp = api_request("POST", url, {"body": comment}, token)
    if resp.get("html_url"):
        print(f"Comment posted: {resp['html_url']}")
        return 0
    print("Failed to post comment")
    return 1


if __name__ == "__main__":
    sys.exit(main())
