# -*- coding: utf-8 -*-
"""functional 测试结果汇总与报告生成（需求 2.7）。

报告输出到仓库根目录 reports/functional/<YYYY-MM-DD>/：
  - results.json  机器可读的完整结果
  - report.md     汇总表格 + 详细表格（Markdown）
  - report.html   汇总表格 + 详细表格（HTML，测试套列合并单元格）

汇总表格列（标题）：
  测试总数 | 测试用例总数 | 测试点总数 | 失败 | 跳过 | 通过 | 通过率

详细表格列（标题）：
  测试套 | 测试用例 | 测试点 | 执行结果 | 失败原因
  其中测试套列相同值合并单元格（HTML 用 rowspan，Markdown 留空）。
"""
from __future__ import annotations

import html
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger("ci_cli.functional.report")

# 状态归类
PASS = "pass"
FAIL = "fail"
SKIP = "skip"
ERROR = "error"

# 中文表头
SUMMARY_HEADERS = ["测试总数", "测试用例总数", "测试点总数", "失败", "跳过", "通过", "通过率"]
DETAIL_HEADERS = ["测试套", "测试用例", "测试点", "执行结果", "失败原因"]

# 状态 -> 中文
STATUS_CN = {
    "pass": "通过",
    "fail": "失败",
    "error": "错误",
    "skip": "跳过",
    "warn": "警告",
}


def summarize_results(all_results: List[Dict]) -> Dict:
    """汇总所有测试套结果。

    all_results: [{"suite","cases":[{"case","status","test_points",...}]}]
    返回：
      {
        "suites_total": N,
        "cases_total": N,
        "points_total": N,
        "pass": N, "fail": N, "skip": N, "error": N,
        "pass_rate": "xx.xx%",
      }
    """
    suites_total = len(all_results)
    cases_total = 0
    points_total = 0
    count = {"pass": 0, "fail": 0, "skip": 0, "error": 0, "warn": 0}

    for suite in all_results:
        for case in suite.get("cases", []):
            cases_total += 1
            points_total += int(case.get("test_points", 0) or 0)
            status = case.get("status", "error")
            count[status] = count.get(status, 0) + 1

    done = count["pass"] + count["fail"] + count["warn"]
    pass_rate = (count["pass"] / done * 100) if done else 0.0

    return {
        "suites_total": suites_total,
        "cases_total": cases_total,
        "points_total": points_total,
        "pass": count["pass"],
        "fail": count["fail"],
        "skip": count["skip"],
        "error": count["error"],
        "pass_rate": f"{pass_rate:.2f}%",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def build_summary_table(summary: Dict) -> str:
    """生成汇总表格（Markdown）。"""
    rows = [
        str(summary["suites_total"]),
        str(summary["cases_total"]),
        str(summary["points_total"]),
        str(summary["fail"]),
        str(summary["skip"]),
        str(summary["pass"]),
        summary["pass_rate"],
    ]
    header = "| " + " | ".join(SUMMARY_HEADERS) + " |"
    sep = "|" + "|".join(["---"] * len(SUMMARY_HEADERS)) + "|"
    data = "| " + " | ".join(rows) + " |"
    return "\n".join([header, sep, data])


def _case_rows(suite: Dict) -> List[Dict]:
    """把套内用例转成详细表格行（含合并所需的 suite 首行标记）。"""
    rows = []
    cases = suite.get("cases", [])
    for idx, case in enumerate(cases):
        rows.append({
            "suite": suite.get("suite", ""),
            "suite_first": idx == 0,          # 该行是套内首行（供合并）
            "case": case.get("case", ""),
            "fmf_path": case.get("fmf_path", ""),
            "test_points": case.get("test_points", 0),
            "status": case.get("status", "error"),
            "fail_reason": case.get("fail_reason", "") or "",
        })
    return rows


def build_detail_md(all_results: List[Dict]) -> str:
    """生成详细表格（Markdown，套列相同值仅首行填写）。"""
    header = "| " + " | ".join(DETAIL_HEADERS) + " |"
    sep = "|" + "|".join(["---"] * len(DETAIL_HEADERS)) + "|"
    lines = [header, sep]

    for suite in all_results:
        rows = _case_rows(suite)
        for row in rows:
            suite_cell = row["suite"] if row["suite_first"] else ""
            status_cn = STATUS_CN.get(row["status"], row["status"])
            reason = (row["fail_reason"] or "").replace("\n", " ").replace("|", "\\|")
            lines.append(
                f"| {suite_cell} | {row['case']} | {row['test_points']} | "
                f"{status_cn} | {reason} |"
            )
    return "\n".join(lines)


def build_detail_html(all_results: List[Dict]) -> str:
    """生成详细表格（HTML，测试套列 rowspan 合并单元格）。"""
    out = []
    out.append('<table border="1" cellspacing="0" cellpadding="4" '
               'style="border-collapse:collapse">')
    out.append("<thead><tr>")
    for h in DETAIL_HEADERS:
        out.append(f"<th style='background:#eee'>{html.escape(h)}</th>")
    out.append("</tr></thead>")
    out.append("<tbody>")

    for suite in all_results:
        rows = _case_rows(suite)
        if not rows:
            continue
        # 套列合并
        out.append("<tr>")
        out.append(f"<td rowspan='{len(rows)}'>{html.escape(rows[0]['suite'])}</td>")
        first = True
        for row in rows:
            if not first:
                out.append("<tr>")
            first = False
            status_cn = STATUS_CN.get(row["status"], row["status"])
            color = {"pass": "green", "fail": "red", "error": "red",
                     "skip": "orange"}.get(row["status"], "")
            style = f" style='color:{color}'" if color else ""
            reason = html.escape(row["fail_reason"] or "")
            out.append(f"<td>{html.escape(row['case'])}</td>")
            out.append(f"<td>{row['test_points']}</td>")
            out.append(f"<td{style}>{html.escape(status_cn)}</td>")
            out.append(f"<td>{reason}</td>")
            out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def build_report(all_results: List[Dict]) -> Dict[str, Path]:
    """生成全部报告文件，返回 {kind: path}。

    输出目录：<repo_root>/reports/functional/<YYYY-MM-DD>/
    """
    summary = summarize_results(all_results)

    md = [
        "# Functional 测试报告",
        "",
        f"- 生成时间: {summary['generated_at']}",
        f"- 测试总数: {summary['suites_total']}",
        f"- 测试用例总数: {summary['cases_total']}",
        f"- 测试点总数: {summary['points_total']}",
        f"- 通过率: {summary['pass_rate']}",
        "",
        "## 汇总",
        "",
        build_summary_table(summary),
        "",
        "## 详细结果",
        "",
        build_detail_md(all_results),
        "",
    ]

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Functional 测试报告 - {summary['generated_at']}</title>
<style>
body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; }}
h1 {{ color: #333; }}
table {{ font-size: 14px; }}
th, td {{ padding: 4px 10px; text-align: left; }}
</style>
</head>
<body>
<h1>Functional 测试报告</h1>
<p>生成时间: {html.escape(summary['generated_at'])}</p>
<p>测试总数: {summary['suites_total']} &nbsp; 测试用例总数: {summary['cases_total']} &nbsp; 测试点总数: {summary['points_total']} &nbsp; 通过率: {summary['pass_rate']}</p>
<h2>汇总</h2>
<table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse">
<thead><tr>{''.join(f"<th style='background:#eee'>{h}</th>" for h in SUMMARY_HEADERS)}</tr></thead>
<tbody>
<tr>{''.join(f"<td>{v}</td>" for v in [summary['suites_total'], summary['cases_total'], summary['points_total'], summary['fail'], summary['skip'], summary['pass'], summary['pass_rate']])}</tr>
</tbody>
</table>
<h2>详细结果</h2>
{build_detail_html(all_results)}
</body>
</html>
"""

    now = datetime.now()
    report_dir = Path.cwd() / "reports" / "functional" / now.strftime("%Y-%m-%d")
    report_dir.mkdir(parents=True, exist_ok=True)

    md_path = report_dir / "report.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    html_path = report_dir / "report.html"
    html_path.write_text(html_doc, encoding="utf-8")

    json_path = report_dir / "results.json"
    payload = {"summary": summary, "suites": all_results}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                         encoding="utf-8")

    logger.info("[report] written: %s / %s / %s", md_path, html_path, json_path)
    return {"md": md_path, "html": html_path, "json": json_path}
