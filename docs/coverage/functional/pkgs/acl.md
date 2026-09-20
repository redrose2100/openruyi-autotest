# ACL Functional Test Coverage Details

**55** test cases in total, **55** test points

| Package | Test Case | Test Point |
|---------|-----------|------------|
| acl | test_acl_getfacl_view_file_default_acl | View file default ACL |
| acl | test_acl_getfacl_view_dir_default_acl | View directory default ACL |
| acl | test_acl_getfacl_param_a_access_acl | Use -a flag to view access ACL |
| acl | test_acl_getfacl_view_default_acl_entries | View directory default ACL entries |
| acl | test_acl_getfacl_param_c_no_header | Use -c flag to hide comment header |
| acl | test_acl_getfacl_param_n_numeric | Use -n flag to display numeric IDs |
| acl | test_acl_getfacl_param_t_tabular | Use -t flag for tabular output |
| acl | test_acl_setfacl_modify_user_rwx | Set rwx permissions for user root |
| acl | test_acl_setfacl_modify_group_rx | Set r-x permissions for group root |
| acl | test_acl_setfacl_modify_other_readonly | Set read-only permissions for other |
| acl | test_acl_setfacl_modify_mask_rwx | Set mask to rwx |
| acl | test_acl_setfacl_param_n_no_recalc_mask | Use -n flag to skip mask recalculation |
| acl | test_acl_setfacl_default_user_acl | Set default user ACL on directory |
| acl | test_acl_setfacl_default_group_acl | Set default group ACL on directory |
| acl | test_acl_setfacl_default_mask | Set default mask on directory |
| acl | test_acl_setfacl_default_other | Set default other on directory |
| acl | test_acl_setfacl_set_replace_acl | Use --set to replace entire ACL |
| acl | test_acl_setfacl_restore_from_rules_file | Read and apply ACL from file |
| acl | test_acl_setfacl_remove_user_entry | Remove user root ACL entry |
| acl | test_acl_setfacl_remove_group_entry | Remove group root ACL entry |
| acl | test_acl_setfacl_remove_all_acl | Remove all extended ACLs |
| acl | test_acl_setfacl_remove_default_acl | Remove directory default ACL |
| acl | test_acl_setfacl_remove_from_rules_file | Remove ACL via rules file |
| acl | test_acl_setfacl_recursive_set | Recursively set ACL on subdirectory files |
| acl | test_acl_setfacl_recursive_remove | Recursively remove ACL from all subdirectory files |
| acl | test_acl_getfacl_backup_file_acl | Backup file ACL |
| acl | test_acl_setfacl_restore_file_acl | Restore file ACL from backup |
| acl | test_acl_getfacl_backup_dir_default_acl | Backup directory default ACL entries |
| acl | test_acl_setfacl_restore_dir_acl | Restore directory ACL from backup |
| acl | test_acl_setfacl_symlink_follow | Use -L flag to follow symlinks when setting ACL |
| acl | test_acl_setfacl_symlink_nofollow | Use -P flag to not follow symlinks |
| acl | test_acl_inheritance_file_inherits_default | New file inherits default ACL |
| acl | test_acl_inheritance_subdir_inherits_default | Subdirectory inherits default ACL |
| acl | test_acl_permission_set_full_acl | Set and verify full ACL permissions |
| acl | test_acl_permission_mask_truncates | Mask limits effective permissions |
| acl | test_acl_permission_mask_restore | Raising mask restores effective permissions |
| acl | test_acl_setfacl_set_named_user_acl | Set named user ACL |
| acl | test_acl_setfacl_recursive_apply_to_subfile | Recursively apply ACL to subfiles |
| acl | test_acl_setfacl_default_and_access_coexist | Default ACL and access ACL coexist on directory |
| acl | test_acl_default_named_user_and_group | Set default ACL named user and group entries |
| acl | test_acl_default_file_inherits_named_entries | New file inherits named default ACL entries |
| acl | test_acl_default_subdir_inherits_named_entries | Subdirectory inherits named default ACL entries |
| acl | test_acl_default_remove_named_user | Remove named user from default ACL |
| acl | test_acl_default_remove_named_group | Remove named group from default ACL |
| acl | test_acl_getfacl_nonexistent_file | getfacl errors on nonexistent file |
| acl | test_acl_setfacl_nonexistent_file | setfacl errors on nonexistent file |
| acl | test_acl_setfacl_invalid_permission | Invalid permission string is rejected |
| acl | test_acl_setfacl_invalid_acl_type | Invalid ACL type tag is rejected |
| acl | test_acl_setfacl_nonexistent_user | Nonexistent user is rejected |
| acl | test_acl_setfacl_nonexistent_group | Nonexistent group is rejected |
| acl | test_acl_setfacl_invalid_perm_string | Invalid permission format is rejected |
| acl | test_acl_setfacl_permission_denied | Permission denied when setting ACL on protected file |
| acl | test_acl_setfacl_multi_user_and_group | Set multi-user and multi-group ACL |
| acl | test_acl_setfacl_export_and_restore | Export and restore ACL |
| acl | test_acl_setfacl_test_dry_run | --test dry-run does not modify ACL |
| | | Verify --test mode did not modify ACL |
