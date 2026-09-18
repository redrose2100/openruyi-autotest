# findutils 功能测试覆盖详情

共 **5** 个测试用例，**13** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| findutils | test_findutils_find | find -name: 按名称查找 |
| | | find -type f: 查找文件 |
| | | find -type d: 查找目录 |
| findutils | test_findutils_find | find -maxdepth: 最大深度 |
| | | find -mindepth: 最小深度 |
| | | find -empty: 空文件/目录 |
| | | find -size: 按大小 |
| findutils | test_findutils_find | find -exec: 执行命令 |
| | | find -delete: 删除文件 |
| | | find -delete: 验证删除 |
| findutils | test_findutils_xargs | xargs: 基本用法 |
| | | xargs -n1: 每次一个参数 |
| findutils | test_findutils_error_handling | find: 无效路径 |
