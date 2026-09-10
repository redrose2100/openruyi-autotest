#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_cloudpods.py

流水线步骤 6：清理流水线创建的 CloudPods 云平台虚拟机（无论成败）。

输入：vm_info.json（含 server_ids）
依赖：tools/cloudpods/create_server.py 中的 CloudPodsClient（复用凭据）
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    """向上查找包含 .git 的目录作为仓库根（兼容 _work/<repo>/<repo> 结构）"""
    for p in [start, *start.parents]:
        if (p / ".git").exists():
            return p
    return start.parents[2] if len(start.parents) >= 3 else start


REPO_ROOT = find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(REPO_ROOT))


def load_create_server(create_server_path: Path):
    spec = importlib.util.spec_from_file_location("create_server", str(create_server_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser(description="Cleanup CloudPods servers created by the pipeline")
    ap.add_argument("--vm-info", required=True, help="Path to vm_info.json")
    ap.add_argument("--create-server", default=None, help="Path to create_server.py")
    args = ap.parse_args()

    with open(args.vm_info, encoding="utf-8") as f:
        vm_info = json.load(f)

    server_ids = vm_info.get("server_ids", [])
    # 防御：某些版本可能带引号（如 'uuid'），统一剥掉
    server_ids = [str(s).strip().strip("'\"").strip() for s in server_ids if str(s).strip()]
    if not server_ids:
        print("No server_ids to clean up")
        return 0

    repo_root = REPO_ROOT
    create_server_path = Path(args.create_server) if args.create_server else (
        repo_root / "tools" / "cloudpods" / "create_server.py"
    )
    mod = load_create_server(create_server_path)
    env_cls = mod.Env

    cp = mod.CloudPodsClient(
        keystone_url=env_cls.cloudpods_keystone_url,
        username=env_cls.cloudpods_user,
        password=mod._decrypt_password(env_cls.cloudpods_password),
    )
    if cp._CloudPodsClient__session is None:
        print("Failed to authenticate with CloudPods")
        return 1

    ok = True
    for sid in server_ids:
        print(f"Deleting server {sid}...")
        if cp.delete_server(sid):
            print(f"  {sid} deleted")
            cp.wait_for_server_is_deleted(sid, timeout=600)
        else:
            print(f"  {sid} delete failed")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
