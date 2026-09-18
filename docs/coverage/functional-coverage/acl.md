# acl 功能测试覆盖详情

共 **55** 个测试用例，**55** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| acl | test_acl_getfacl_view_file_default_acl | 查看文件默认 ACL |
| acl | test_acl_getfacl_view_dir_default_acl | 查看目录默认 ACL |
| acl | test_acl_getfacl_param_a_access_acl | 使用 -a 参数查看 access ACL |
| acl | test_acl_getfacl_view_default_acl_entries | 查看目录默认 ACL 条目 |
| acl | test_acl_getfacl_param_c_no_header | 使用 -c 参数不显示注释头 |
| acl | test_acl_getfacl_param_n_numeric | 使用 -n 参数显示数字 ID |
| acl | test_acl_getfacl_param_t_tabular | 使用 -t 参数表格输出 |
| acl | test_acl_setfacl_modify_user_rwx | 设置用户 root 的 rwx 权限 |
| acl | test_acl_setfacl_modify_group_rx | 设置组 root 的 r-x 权限 |
| acl | test_acl_setfacl_modify_other_readonly | 设置 other 的只读权限 |
| acl | test_acl_setfacl_modify_mask_rwx | 设置 mask 为 rwx |
| acl | test_acl_setfacl_param_n_no_recalc_mask | 使用 -n 参数不重新计算 mask |
| acl | test_acl_setfacl_default_user_acl | 为目录设置 default user ACL |
| acl | test_acl_setfacl_default_group_acl | 为目录设置 default group ACL |
| acl | test_acl_setfacl_default_mask | 为目录设置 default mask |
| acl | test_acl_setfacl_default_other | 为目录设置 default other |
| acl | test_acl_setfacl_set_replace_acl | 使用 --set 替换整个 ACL |
| acl | test_acl_setfacl_restore_from_rules_file | 从文件读取并应用 ACL |
| acl | test_acl_setfacl_remove_user_entry | 删除用户 root 的 ACL 条目 |
| acl | test_acl_setfacl_remove_group_entry | 删除组 root 的 ACL 条目 |
| acl | test_acl_setfacl_remove_all_acl | 删除所有扩展 ACL |
| acl | test_acl_setfacl_remove_default_acl | 删除目录的 default ACL |
| acl | test_acl_setfacl_remove_from_rules_file | 通过规则文件删除 ACL |
| acl | test_acl_setfacl_recursive_set | 递归设置子目录文件 ACL |
| acl | test_acl_setfacl_recursive_remove | 递归删除所有子目录文件 ACL |
| acl | test_acl_getfacl_backup_file_acl | 备份文件 ACL |
| acl | test_acl_setfacl_restore_file_acl | 从备份恢复文件 ACL |
| acl | test_acl_getfacl_backup_dir_default_acl | 备份目录 default ACL 条目 |
| acl | test_acl_setfacl_restore_dir_acl | 从备份恢复目录 ACL |
| acl | test_acl_setfacl_symlink_follow | 使用 -L 参数跟随符号链接设置 ACL |
| acl | test_acl_setfacl_symlink_nofollow | 使用 -P 参数不跟随符号链接 |
| acl | test_acl_inheritance_file_inherits_default | 新文件继承 default ACL |
| acl | test_acl_inheritance_subdir_inherits_default | 子目录继承 default ACL |
| acl | test_acl_permission_set_full_acl | 设置并验证完整 ACL 权限 |
| acl | test_acl_permission_mask_truncates | mask 限制有效权限 |
| acl | test_acl_permission_mask_restore | 提升 mask 恢复有效权限 |
| acl | test_acl_setfacl_set_named_user_acl | 设置命名用户 ACL |
| acl | test_acl_setfacl_recursive_apply_to_subfile | 递归应用 ACL 到子文件 |
| acl | test_acl_setfacl_default_and_access_coexist | 目录上 default ACL 与 access ACL 共存 |
| acl | test_acl_default_named_user_and_group | 设置 default ACL 命名用户和组条目 |
| acl | test_acl_default_file_inherits_named_entries | 新文件继承命名 default ACL 条目 |
| acl | test_acl_default_subdir_inherits_named_entries | 子目录继承命名 default ACL 条目 |
| acl | test_acl_default_remove_named_user | 从 default ACL 中删除命名用户 |
| acl | test_acl_default_remove_named_group | 从 default ACL 中删除命名组 |
| acl | test_acl_getfacl_nonexistent_file | 对不存在的文件执行 getfacl 报错 |
| acl | test_acl_setfacl_nonexistent_file | 对不存在的文件执行 setfacl 报错 |
| acl | test_acl_setfacl_invalid_permission | 无效权限字符串被拒绝 |
| acl | test_acl_setfacl_invalid_acl_type | 无效 ACL 类型标记被拒绝 |
| acl | test_acl_setfacl_nonexistent_user | 不存在用户被拒绝 |
| acl | test_acl_setfacl_nonexistent_group | 不存在组被拒绝 |
| acl | test_acl_setfacl_invalid_perm_string | 无效权限格式被拒绝 |
| acl | test_acl_setfacl_permission_denied | 无权限设置受保护文件 ACL |
| acl | test_acl_setfacl_multi_user_and_group | 设置多用户和多组 ACL |
| acl | test_acl_setfacl_export_and_restore | 导出并恢复 ACL |
| acl | test_acl_setfacl_test_dry_run | --test 模拟运行不修改 ACL |
| | | 验证 --test 模式未修改 ACL |
