# -*- coding: utf-8 -*-
"""
cloudpods 包：CloudPods 云平台 + openRuyi QEMU 环境创建核心库。

由 tools/cloudpods/create_server.py 复制而来，作为新架构的库被命令使用。
原脚本入口 (if __name__ == "__main__") 在复制时保留，但 CI 统一通过
scripts 的 cli.py 调用 commands/launch_qemu_env.py 等命令。
"""
