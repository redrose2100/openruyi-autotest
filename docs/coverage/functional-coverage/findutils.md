# findutils 功能测试覆盖详情

共 **5** 个测试套，**13** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_findutils_find | 3 cases | find -name: 按名称查找 |
| | | find -type f: 查找文件 |
| | | find -type d: 查找目录 |
| test_findutils_find | 4 cases | find -maxdepth: 最大深度 |
| | | find -mindepth: 最小深度 |
| | | find -empty: 空文件/目录 |
| | | find -size: 按大小 |
| test_findutils_find | 3 cases | find -exec: 执行命令 |
| | | find -delete: 删除文件 |
| | | find -delete: 验证删除 |
| test_findutils_xargs | 2 cases | xargs: 基本用法 |
| | | xargs -n1: 每次一个参数 |
| test_findutils_error_handling | 1 cases | find: 无效路径 |
