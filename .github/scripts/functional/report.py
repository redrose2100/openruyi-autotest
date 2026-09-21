# -*- coding: utf-8 -*-
"""Functional test result aggregation and report generation (requirement 2.7).

Reports output to repo root reports/functional/<YYYY-MM-DD>/:
  - results.json  machine-readable full results
  - report.md     summary table + detail table (Markdown)
  - report.html   summary table + detail table (HTML, test suite column merged cells)

Summary table columns (headers):
  Total Tests | Total Test Cases | Total Test Points | Failed | Skipped | Passed | Pass Rate

Detail table columns (headers):
  Test Suite | Test Case | Test Point | Result | Failure Reason
  Test suite column merges cells for same value (HTML rowspan, Markdown blank).
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

# Status classification
PASS = "pass"
FAIL = "fail"
SKIP = "skip"
ERROR = "error"

# English headers
SUMMARY_HEADERS = ["Total Tests", "Total Cases", "Total Points", "Failed", "Skipped", "Passed", "Pass Rate"]
DETAIL_HEADERS = ["Test Suite", "Test Case", "Test Point", "Result", "Failure Reason"]

# Status → label
STATUS_LABEL = {
    "pass": "Passed",
    "fail": "Failed",
    "error": "Error",
    "skip": "Skipped",
    "warn": "Warning",
}


def summarize_results(all_results: List[Dict]) -> Dict:
    """Aggregate results of all test suites.

    all_results: [{"suite","cases":[{"case","status","test_points",...}]}]
    Returns:
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
    """Generate summary table (Markdown)."""
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
    """Convert cases in a suite to detail table rows (includes suite first-row marker for merging)."""
    rows = []
    cases = suite.get("cases", [])
    for idx, case in enumerate(cases):
        rows.append({
            "suite": suite.get("suite", ""),
            "suite_first": idx == 0,          # first row in suite (for cell merging)
            "case": case.get("case", ""),
            "fmf_path": case.get("fmf_path", ""),
            "test_points": case.get("test_points", 0),
            "status": case.get("status", "error"),
            "fail_reason": case.get("fail_reason", "") or "",
        })
    return rows


def build_detail_md(all_results: List[Dict]) -> str:
    """Generate detail table (Markdown, suite column same value only shown on first row)."""
    header = "| " + " | ".join(DETAIL_HEADERS) + " |"
    sep = "|" + "|".join(["---"] * len(DETAIL_HEADERS)) + "|"
    lines = [header, sep]

    for suite in all_results:
        rows = _case_rows(suite)
        for row in rows:
            suite_cell = row["suite"] if row["suite_first"] else ""
            status_label = STATUS_LABEL.get(row["status"], row["status"])
            reason = (row["fail_reason"] or "").replace("\n", " ").replace("|", "\\|")
            lines.append(
                f"| {suite_cell} | {row['case']} | {row['test_points']} | "
                f"{status_label} | {reason} |"
            )
    return "\n".join(lines)


def build_detail_html(all_results: List[Dict]) -> str:
    """Generate detail table (HTML, suite column rowspan merged cells)."""
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
        # Suite column merge
        out.append("<tr>")
        out.append(f"<td rowspan='{len(rows)}'>{html.escape(rows[0]['suite'])}</td>")
        first = True
        for row in rows:
            if not first:
                out.append("<tr>")
            first = False
            status_label = STATUS_LABEL.get(row["status"], row["status"])
            color = {"pass": "green", "fail": "red", "error": "red",
                     "skip": "orange"}.get(row["status"], "")
            style = f" style='color:{color}'" if color else ""
            reason = html.escape(row["fail_reason"] or "")
            out.append(f"<td>{html.escape(row['case'])}</td>")
            out.append(f"<td>{row['test_points']}</td>")
            out.append(f"<td{style}>{html.escape(status_label)}</td>")
            out.append(f"<td>{reason}</td>")
            out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def build_report(all_results: List[Dict]) -> Dict[str, Path]:
    """Generate all report files, returns {kind: path}.

    Output directory: <repo_root>/reports/functional/<YYYY-MM-DD>/
    """
    summary = summarize_results(all_results)

    md = [
        "# Functional Test Report",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Total Suites: {summary['suites_total']}",
        f"- Total Cases: {summary['cases_total']}",
        f"- Total Points: {summary['points_total']}",
        f"- Pass Rate: {summary['pass_rate']}",
        "",
        "## Summary",
        "",
        build_summary_table(summary),
        "",
        "## Details",
        "",
        build_detail_md(all_results),
        "",
    ]

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Functional Test Report - {summary['generated_at']}</title>
<style>
body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; }}
h1 {{ color: #333; }}
table {{ font-size: 14px; }}
th, td {{ padding: 4px 10px; text-align: left; }}
</style>
</head>
<body>
<h1>Functional Test Report</h1>
<p>Generated: {html.escape(summary['generated_at'])}</p>
<p>Total Suites: {summary['suites_total']} &nbsp; Total Cases: {summary['cases_total']} &nbsp; Total Points: {summary['points_total']} &nbsp; Pass Rate: {summary['pass_rate']}</p>
<h2>Summary</h2>
<table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse">
<thead><tr>{''.join(f"<th style='background:#eee'>{h}</th>" for h in SUMMARY_HEADERS)}</tr></thead>
<tbody>
<tr>{''.join(f"<td>{v}</td>" for v in [summary['suites_total'], summary['cases_total'], summary['points_total'], summary['fail'], summary['skip'], summary['pass'], summary['pass_rate']])}</tr>
</tbody>
</table>
<h2>Details</h2>
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
