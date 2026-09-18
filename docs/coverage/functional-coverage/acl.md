# acl 功能测试覆盖详情

共 **10** 个测试用例，**81** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| acl | test_acl_getfacl_basic | 查看文件默认 ACL |
| | | 查看目录默认 ACL |
| | | 使用 -a 参数查看 access ACL |
| | | 使用 -d 参数查看 default ACL |
| | | 使用 -c 参数不显示注释头 |
| | | 使用 -n 参数显示数字 ID |
| | | 使用 -t 参数表格输出 |
| acl | test_acl_setfacl_basic | 设置用户 root 的 rwx 权限 |
| | | 验证 ACL 设置 |
| | | 设置组 root 的 r-x 权限 |
| | | 验证 ACL 设置 |
| | | 设置 other 的只读权限 |
| | | 验证 ACL 设置 |
| | | 设置 mask 为 rwx |
| | | 验证 mask 设置 |
| | | 使用 -n 参数不重新计算 mask |
| | | 验证 ACL 设置 |
| acl | test_acl_setfacl_advanced | 为目录设置 default user ACL |
| | | 验证 default ACL 设置 |
| | | 为目录设置 default group ACL |
| | | 验证 default group ACL |
| | | 为目录设置 default mask |
| | | 验证 default mask |
| | | 为目录设置 default other |
| | | 验证 default other |
| | | 使用 --set 替换整个 ACL |
| | | 验证 ACL 替换 |
| | | 创建 ACL 规则文件 |
| | | 从文件读取并应用 ACL |
| | | 验证从文件应用的 ACL |
| acl | test_acl_setfacl_remove | 删除用户 root 的 ACL 条目 |
| | | 验证 ACL 删除 |
| | | 删除组 root 的 ACL 条目 |
| | | 验证 ACL 删除 |
| | | 删除所有扩展 ACL |
| | | 验证所有扩展 ACL 已删除 |
| | | 删除目录的 default ACL |
| | | 验证 default ACL 已删除 |
| | | 创建删除规则文件 |
| | | 先添加用户 ACL |
| | | 从文件读取并删除 ACL |
| | | 验证从文件删除的 ACL |
| acl | test_acl_setfacl_recursive | 创建多层子目录 |
| | | 创建测试文件 |
| | | 递归设置 user ACL |
| | | 验证递归设置 - file1 |
| | | 验证递归设置 - file2 |
| | | 递归删除所有扩展 ACL |
| | | 验证递归删除 - file1 |
| | | 验证递归删除 - file2 |
| acl | test_acl_setfacl_symlink | 创建符号链接 |
| | | 使用 -L 跟随符号链接设置 ACL |
| | | 验证符号链接目标文件的 ACL |
| | | 使用 -P 不跟随符号链接 |
| acl | test_acl_chacl | 先清理 ACL |
| | | 使用 chacl 查看 ACL |
| | | 使用 chacl 设置基本 ACL |
| | | 验证 chacl 设置的 ACL |
| | | 使用 chacl 设置 default ACL |
| | | 验证 chacl 设置的 default ACL |
| | | 使用 chacl 递归设置 ACL |
| | | 验证 chacl 递归设置 |
| | | 使用 chacl -b 同时设置 |
| | | 验证 chacl -b 设置 |
| acl | test_acl_inheritance | 设置目录 default ACL |
| | | 在目录中创建新文件 |
| | | 验证新文件继承了 default ACL |
| | | 在目录中创建子目录 |
| | | 验证子目录继承了 default ACL |
| acl | test_acl_permission_verify | 设置完整权限 |
| | | 验证权限设置 |
| | | 设置 mask 限制有效权限 |
| | | 验证 mask 限制后的有效权限 |
| acl | test_acl_special_cases | 设置多个用户和组 ACL |
| | | 验证多个 ACL 条目 |
| | | 设置测试 ACL |
| | | 导出 ACL 备份 |
| | | 清除 ACL |
| | | 尝试恢复 ACL |
| | | 使用 --test 模式不实际修改 |
| | | 验证 --test 模式未修改 ACL |
