# Python 编码规范

> `tools/` 和 `unittests/` 目录下 Python 代码的编码标准。

---

## 文件结构

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块文档字符串：描述本模块的用途。

用法示例或关键说明。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional


def main() -> int:
    """入口函数，返回退出码。"""
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 要求

- ✅ 文件头使用 `# -*- coding: utf-8 -*-`
- ✅ 顶层使用 `from __future__ import annotations`
- ✅ 模块级 `__doc__`（文档字符串）
- ✅ `main()` 函数返回 `int`（0 成功，非 0 失败）
- ❌ 避免在模块顶层执行副作用代码（用 `if __name__ == "__main__"` 保护）

---

## 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| 模块/文件 | `snake_case` | `test_fmf_metadata.py` |
| 类 | `PascalCase` | `TestFmfYamlValid` |
| 函数/方法 | `snake_case` | `collect_real_test_dirs()` |
| 常量 | `UPPER_SNAKE_CASE` | `VALID_TIERS` |
| 变量 | `snake_case` | `failures`, `test_dir` |

---

## 类型注解

所有公共函数应有类型注解：

```python
from pathlib import Path

def collect_test_dirs(base: Path) -> list[Path]:
    """收集所有测试目录。"""
    ...
```

- 使用 `Path` 代替 `str` 处理路径
- 工具函数返回值必须注解
- 可选值使用 `Optional[X]` 或 `X | None`

---

## 导入顺序

1. `from __future__` 导入
2. 标准库
3. 第三方库
4. 本地模块

```python
from __future__ import annotations

import os
import unittest
from pathlib import Path

import yaml

from unittests import tmt_utils
```

---

## 测试规范（unittests/）

- 使用 `unittest` 或 `pytest` 框架
- 测试类命名：`Test<描述>`
- 测试方法命名：`test_<描述>`
- 使用 `self.skipTest()` 处理条件跳过（如缺少 bash 时）

```python
class TestFmfMetadata(unittest.TestCase):
    def test_all_main_fmf_valid_yaml(self):
        violations = []
        for test_dir in tmt_utils.collect_real_test_dirs():
            ...
        if violations:
            self.fail("\n".join(violations))
```

---

## 禁止事项

- ❌ 硬编码绝对路径（使用 `Path` 相对路径或 `tmt_utils.TESTS_DIR`）
- ❌ `except:` 裸异常（至少指定 `except Exception`）
- ❌ `print()` 用于日志（使用 `logging` 或 `unittest` 断言）
- ❌ 在仓库中公开敏感凭证