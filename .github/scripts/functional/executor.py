# -*- coding: utf-8 -*-
"""functional 测试套执行器。

对单个测试套（如 acl）在已申请的环境（QEMU VM）中执行其全部用例：

  1. 将仓库打包（排除 docs/.github/unittests 等）并上传到环境
  2. 在 QEMU 内准备执行环境（tmt / beakerlib，复用 run_tests_in_qemu 逻辑）
  3. 配置 topology.env（指向本机）
  4. 以 tmt 执行该测试套（--name /tests/functional/pkgs/<suite>）：
     - 套级用例（套目录自身的 test.sh）作为套内 case
     - 子用例 test_* 各自执行
  5. 解析输出得到每个用例的 pass/fail/error/skip 与功能点明细

复用 run_tests_in_qemu 的：remote_prepare_env / remote_setup_topology /
run_tmt_tests（按 --name 过滤）/ run_tests_direct（tmt 不可用时）。
"""
from __future__ import annotations

import json
import logging
import os
import re
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.ssh import SSHClient

logger = logging.getLogger("ci_cli.functional.executor")

# 复用 run_tests_in_qemu 的远程准备/执行函数
from commands.run_tests_in_qemu import (
    _setup_ruamel_pure_python,
    remote_prepare_env,
    remote_setup_topology,
    run_tests_direct,
)

_REMOTE_DIR = "/home/openruyi/openruyi-autotest"


def package_repo(repo_root: Path, excludes: Optional[List[str]] = None) -> str:
    """把仓库打包为 tar.gz（排除 .git 与无关目录），返回临时文件路径。"""
    fd, tmp = tempfile.mkstemp(suffix=".tar.gz")
    os.close(fd)

    base_excludes = [".git", "docs", ".github", "unittests"]
    if excludes:
        base_excludes = list(dict.fromkeys(base_excludes + list(excludes)))
    with tarfile.open(tmp, "w:gz") as tar:
        for child in sorted(repo_root.iterdir()):
            if child.name in base_excludes:
                continue
            tar.add(child, arcname=f"openruyi-autotest/{child.name}")
    return tmp


def _exec3(ssh: SSHClient, cmd: str, **kw):
    r = ssh.exec(cmd, **kw)
    return r.code, r.stdout, r.stderr


def ensure_tar(ssh: SSHClient, ssh_pw: str) -> bool:
    """确保 QEMU 内有 tar（最小系统可能缺失）。"""
    ssh.exec(f"echo '{ssh_pw}' | sudo -S true")
    code, out, err = _exec3(ssh, "command -v tar", timeout=30)
    if code == 0:
        return True
    code, out, err = _exec3(ssh,
        f"echo '{ssh_pw}' | sudo -S dnf install -y "
        "--nogpgcheck --setopt=sslverify=0 tar gzip 2>&1 | tail -5",
        timeout=600)
    code, out, err = _exec3(ssh, "command -v tar", timeout=30)
    return code == 0


def upload_repo(ssh: SSHClient, tarball: str, ssh_pw: str) -> bool:
    """上传并解压仓库到 QEMU 内固定目录。"""
    ssh.exec(f"rm -rf {_REMOTE_DIR}")
    ssh.exec("mkdir -p /home/openruyi")
    if not ssh.put_file(tarball, "/home/openruyi/repo.tar.gz"):
        logger.error("[exec] upload repo failed")
        return False
    code, out, err = _exec3(ssh,
        "cd /home/openruyi && tar xzf repo.tar.gz && rm -f repo.tar.gz",
        timeout=300)
    if code != 0:
        logger.error("[exec] extract failed: %s %s", out[-300:], err[-300:])
        return False
    return True


def run_suite_on_env(
    ssh: SSHClient,
    ssh_pw: str,
    suite_fmf_path: str,
    cases: List[Dict],
    suite_name: str,
    timeout: int = 5400,
) -> Dict:
    """在已连接的环境上执行一个测试套的全部用例。

    suite_fmf_path: 套的 fmf path（/tests/functional/pkgs/acl）
    cases: 套下所有用例 dict 列表，每项含
           {"case", "fmf_path", "test_points", ...}

    返回结果 dict：
      {
        "suite": suite_name,
        "cases": [{"case","fmf_path","status","test_points","fail_reason","output"}],
        "exec_mode": "tmt"|"direct"|"",
      }
    """
    result: Dict = {
        "suite": suite_name,
        "cases": [],
        "exec_mode": "",
        "error": None,
    }

    # 1. 准备执行环境（tmt/beakerlib）
    exec_mode = remote_prepare_env(ssh, ssh_pw)
    if not exec_mode:
        result["error"] = "prepare env failed"
        logger.error("[exec] %s: prepare env failed", suite_name)
        return result
    result["exec_mode"] = exec_mode

    # 2. 配置 topology.env（指向本机）
    remote_setup_topology(ssh, ssh_pw, "127.0.0.1")

    case_fmf_paths = [c["fmf_path"] for c in cases]

    # 3. 执行：tmt 或 direct
    suite_results: List[Dict] = []
    try:
        if exec_mode == "tmt":
            suite_results = _run_tmt_suite(ssh, ssh_pw, suite_fmf_path,
                                           case_fmf_paths, timeout)
        else:
            suite_results = _run_direct_suite(ssh, ssh_pw, suite_fmf_path,
                                              case_fmf_paths, timeout)
    except Exception as exc:  # noqa: BLE001
        # 单个用例失败不应丢弃整套已执行结果：记录异常并继续归一化
        logger.error("[exec] %s: suite execution raised, "
                     "keeping %d partial result(s): %s",
                     suite_name, len(suite_results), exc)
        result["error"] = f"partial: {exc}"

    # 4. 归一化结果（补全 fail_reason / test_points）
    case_by_path = {c["fmf_path"]: c for c in cases}
    for r in suite_results:
        case = case_by_path.get(r["fmf_path"], {})
        item = {
            "case": case.get("case", r["fmf_path"].rsplit("/", 1)[-1]),
            "fmf_path": r["fmf_path"],
            "status": r["status"],
            "test_points": case.get("test_points", 0),
            "fail_reason": r.get("fail_reason", ""),
            "output": r.get("output", ""),
        }
        result["cases"].append(item)

    return result


def _run_tmt_suite(ssh: SSHClient, ssh_pw: str, suite_fmf_path: str,
                   case_fmf_paths: List[str], timeout: int) -> List[Dict]:
    """用 tmt 执行整个测试套（套自身 + 所有子用例）。"""
    results: List[Dict] = []
    # tmt --name 匹配子树：传套路径即可覆盖所有子用例
    cmd = (
        f"cd {_REMOTE_DIR} && "
        f"echo '{ssh_pw}' | sudo -S true && "
        f"timeout {timeout} tmt run --all plan --name /plans/functional "
        f"--name {suite_fmf_path} provision --feeling-safe 2>&1"
    )
    logger.info("[exec] %s: running tmt suite: %s...", suite_fmf_path, cmd[:300])
    code, out, err = _exec3(ssh, cmd, timeout=timeout + 60)
    output = out + ("\n[stderr]\n" + err if err else "")
    logger.info("[exec] %s: tmt exit=%s, output len=%s", suite_fmf_path, code,
                len(output))

    # 解析 tmt 树状输出中的用例状态
    parsed = _parse_tmt_output(output, case_fmf_paths)
    if parsed:
        return parsed

    # 解析失败：整套标记
    status = "fail" if (code != 0 or "fail" in output.lower()) else "pass"
    results.append({
        "fmf_path": suite_fmf_path,
        "status": status,
        "fail_reason": "tmt output unparsed" if status == "fail" else "",
        "output": output[-4000:],
    })
    return results


def _parse_tmt_output(output: str, case_fmf_paths: List[str]) -> List[Dict]:
    """解析 tmt 树状输出，返回每个用例的结果。"""
    results: List[Dict] = []
    lines = output.splitlines()
    current_test = None
    current_fail_reason: List[str] = []
    # 干扰行前缀（tmt 各阶段标题等），排除这些不当作失败原因
    _NOISE = (
        "discover", "provision", "prepare", "execute", "report", "plan",
        "summary", "1 test", "total", "Result", "How", "finish",
    )
    pending_result: Optional[Dict] = None  # 等待捕获失败详情的已解析结果
    for line in lines:
        m = re.match(r"^\s*(/tests/\S+)\s*$", line)
        if m:
            current_test = m.group(1)
            current_fail_reason = []
            pending_result = None
            continue
        if current_test:
            m2 = re.match(r"^\s*(pass|fail|error|skip|warn)\s*$", line)
            if m2:
                res = {
                    "fmf_path": current_test,
                    "status": m2.group(1),
                    "fail_reason": "",
                    "output": "",
                }
                results.append(res)
                # 若失败，后续行可能是失败详情（output: ...），挂起等待捕获
                if m2.group(1) in ("fail", "error"):
                    pending_result = res
                else:
                    pending_result = None
                    current_test = None
                continue
            # 捕获挂起中的失败详情
            if pending_result is not None:
                stripped = line.strip()
                if stripped and (stripped.startswith("output:")
                                 or stripped.startswith("/tmp/")
                                 or stripped.startswith("::")):
                    current_fail_reason.append(stripped)
                    pending_result["fail_reason"] = " | ".join(current_fail_reason)[:1000]
                elif not stripped:
                    continue
                else:
                    # 非详情行（下一阶段标题等）停止捕获
                    pending_result = None
                    current_test = None
                    continue
            elif line.strip():
                stripped = line.strip()
                if not stripped.startswith(_NOISE):
                    pass  # 其他行忽略

    # 过滤：只保留本套内的用例
    valid = [r for r in results if r["fmf_path"] in set(case_fmf_paths) or
             r["fmf_path"].startswith("/tests/functional/pkgs/")]
    # 补充未出现在输出中的用例（标记为 error）
    covered = {r["fmf_path"] for r in valid}
    for p in case_fmf_paths:
        if p not in covered:
            valid.append({
                "fmf_path": p,
                "status": "error",
                "fail_reason": "no tmt output for this case",
                "output": "",
            })
    return valid


def _run_direct_suite(ssh: SSHClient, ssh_pw: str, suite_fmf_path: str,
                      case_fmf_paths: List[str], timeout: int) -> List[Dict]:
    """tmt 不可用时直接以 beakerlib 方式执行每个用例脚本。

    逐用例执行：单个用例超时/异常只标记该用例为 error，
    不中断整个套，保证已完成的用例结果不会丢失。
    """
    normalized: List[Dict] = []
    for path in case_fmf_paths:
        try:
            results = run_tests_direct(
                ssh, ssh_pw,
                repo_dir=_REMOTE_DIR,
                test_paths=[path],
                suite_paths=[],
                timeout=timeout,
            )
            for r in results:
                normalized.append({
                    "fmf_path": r["test_path"],
                    "status": r["status"],
                    "fail_reason": "" if r["status"] == "pass"
                    else (r.get("final_result") or "failed"),
                    "output": r.get("output", ""),
                })
        except Exception as exc:  # noqa: BLE001
            logger.error("[exec] %s: case %s failed with exception, "
                         "marking as error: %s", suite_fmf_path, path, exc)
            normalized.append({
                "fmf_path": path,
                "status": "error",
                "fail_reason": f"execution raised: {exc}",
                "output": "",
            })
    return normalized
