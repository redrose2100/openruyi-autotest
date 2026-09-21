# -*- coding: utf-8 -*-
"""
cloudpods package: CloudPods cloud platform + openRuyi QEMU env creation core lib.

Copied from tools/cloudpods/create_server.py, used as a library by commands in
the new architecture. The original script entry point (if __name__ == "__main__")
is preserved in the copy, but CI uniformly calls commands/launch_qemu_env.py etc.
via scripts cli.py.
"""
