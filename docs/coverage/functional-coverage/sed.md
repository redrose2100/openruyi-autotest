# sed 功能测试覆盖详情

共 **6** 个测试用例，**12** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| sed | test_sed_basic_substitution | sed s: 基本替换 |
| | | sed s: 替换hello |
| sed | test_sed_line_operations | sed -n: 打印指定行 |
| | | sed d: 删除指定行 |
| | | sed a: 追加行 |
| | | sed i: 插入行 |
| sed | test_sed_global_regex | sed g: 全局替换 |
| | | sed: 正则替换 |
| sed | test_sed_basic | sed -i: 就地编辑 |
| | | sed -i: 验证修改 |
| sed | test_sed_basic | sed -e: 多表达式 |
| sed | test_sed_error_handling | sed: 无效选项 |
