# 测试用例编写规范

> 本目录包含编写 openEuler RISC-V 自动化测试用例的核心规范。

---

## 概述

本项目基于 **TMT (Test Management Tool)** + **Beakerlib** 框架，测试用例分布在 `tests/` 下按类别组织。

---

## 规范索引

| 规范 | 说明 | 状态 |
|------|------|------|
| [Beakerlib 测试模式](./beakerlib-patterns.md) | rlRun / rlPhase / rlJournal 生命周期规范 | 已填写 |
| [FMF 元数据规范](./fmf-metadata.md) | main.fmf 字段约定（tier/duration/test 等） | 已填写 |
| [Shell 脚本规范](./shell-coding.md) | bash 编码、shebang、语法检查标准 | 已填写 |
| [测试质量标准](./test-quality.md) | 边界用例、正反向测试、中文字符检查 | 已填写 |

---

## 快速参考

### 测试目录结构（以 coreutils 为例）

```
tests/functional/pkgs/coreutils/
├── main.fmf                          # 包级共享配置
├── lib.sh                            # 包级共享函数
├── test_coreutils_b2sum_and_sum/     # 单个功能点 = 一个目录
│   └── test.sh                       # 测试脚本（唯一入口）
├── test_coreutils_basic_file_ops/
│   └── test.sh
└── test_coreutils_error_handling/
    └── test.sh
```

### 原则

- **一个文件 = 一个功能点**：每个测试目录只测一个独立功能
- **失败能定位**：单测失败直接指向具体功能，无需翻日志
- **Beakerlib 三阶段**：Setup → Test → Cleanup，缺一不可
- **中文文档**：所有规范文档使用中文编写