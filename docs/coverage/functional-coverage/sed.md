# sed 功能测试覆盖详情

共 **6** 个测试套，**12** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_sed_basic_substitution | 2 cases | sed s: 基本替换 |
| | | sed s: 替换hello |
| test_sed_line_operations | 4 cases | sed -n: 打印指定行 |
| | | sed d: 删除指定行 |
| | | sed a: 追加行 |
| | | sed i: 插入行 |
| test_sed_global_regex | 2 cases | sed g: 全局替换 |
| | | sed: 正则替换 |
| test_sed_basic | 2 cases | sed -i: 就地编辑 |
| | | sed -i: 验证修改 |
| test_sed_basic | 1 cases | sed -e: 多表达式 |
| test_sed_error_handling | 1 cases | sed: 无效选项 |
