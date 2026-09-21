# -*- coding: utf-8 -*-
"""
GitHub API wrapper (uses requests to avoid urllib dropping auth on 302 redirects).
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

GITHUB_API = "https://api.github.com"


class GitHubClient:
    """GitHub REST API lightweight wrapper."""

    def __init__(
        self,
        token: Optional[str] = None,
        repository: Optional[str] = None,
        pr_number: Optional[str] = None,
    ):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        self.repository = repository or os.environ.get("GITHUB_REPOSITORY", "")
        self.pr_number = pr_number or os.environ.get("PR_NUMBER", "")

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @property
    def configured(self) -> bool:
        return bool(self.token and self.repository and self.pr_number)

    # ------------------------------------------------------------------
    # Basic request
    # ------------------------------------------------------------------
    def request(self, method: str, path: str, body: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        url = path if path.startswith("http") else f"{GITHUB_API}/repos/{self.repository}{path}"
        try:
            resp = requests.request(method, url, headers=self.headers, json=body, timeout=30)
            if resp.status_code >= 400:
                print(
                    f"API error {resp.status_code} for {method} {url}: "
                    f"{resp.text[:500]}"
                )
                return None
            return resp.json() if resp.text else {}
        except Exception as exc:  # noqa: BLE001
            print(f"API request failed: {exc}")
            return None

    def get(self, path: str) -> Optional[Dict[str, Any]]:
        return self.request("GET", path)

    def post(self, path: str, body: Dict) -> Optional[Dict[str, Any]]:
        return self.request("POST", path, body)

    # ------------------------------------------------------------------
    # Comments
    # ------------------------------------------------------------------
    def post_pr_comment(self, body: str) -> Optional[str]:
        """Post a PR comment; returns html_url on success."""
        if not self.configured:
            print("Missing GITHUB_TOKEN / GITHUB_REPOSITORY / PR_NUMBER")
            return None
        resp = self.post(f"/issues/{self.pr_number}/comments", {"body": body})
        if resp and resp.get("html_url"):
            return resp["html_url"]
        return None
