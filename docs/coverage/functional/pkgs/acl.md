# acl Functional Test Coverage Details

**55** test cases in total, **55** test points

| Package | Test Case | Test Point |
|---------|-----------|------------|
| acl | test_acl_default_file_inherits_named_entries | default ACL - new file inherits named entries |
| acl | test_acl_default_named_user_and_group | default ACL - set named user and group entries |
| acl | test_acl_default_remove_named_group | default ACL - remove named group from default ACL |
| acl | test_acl_default_remove_named_user | default ACL - remove named user from default ACL |
| acl | test_acl_default_subdir_inherits_named_entries | default ACL - subdirectory inherits named default entries |
| acl | test_acl_getfacl_backup_dir_default_acl | getfacl backup - save directory default ACL |
| acl | test_acl_getfacl_backup_file_acl | getfacl backup - save file ACL to backup |
| acl | test_acl_getfacl_nonexistent_file | getfacl - error on nonexistent file |
| acl | test_acl_getfacl_param_a_access_acl | getfacl -a show access ACL only |
| acl | test_acl_getfacl_param_c_no_header | getfacl -c suppress header comment |
| acl | test_acl_getfacl_param_n_numeric | getfacl -n display numeric UID/GID |
| acl | test_acl_getfacl_param_t_tabular | getfacl -t tabular output format |
| acl | test_acl_getfacl_view_default_acl_entries | getfacl - view default ACL entries on directory |
| acl | test_acl_getfacl_view_dir_default_acl | getfacl - view directory default ACL |
| acl | test_acl_getfacl_view_file_default_acl | getfacl - view file default ACL |
| acl | test_acl_inheritance_file_inherits_default | ACL inheritance - new file inherits default ACL |
| acl | test_acl_inheritance_subdir_inherits_default | ACL inheritance - subdirectory inherits default ACL |
| acl | test_acl_permission_mask_restore | ACL permission - raise mask restores effective permissions |
| acl | test_acl_permission_mask_truncates | ACL permission - mask truncates effective permissions |
| acl | test_acl_permission_set_full_acl | ACL permission - set and verify full ACL entries |
| acl | test_acl_setfacl_default_and_access_coexist | setfacl - default and access ACL coexist on directory |
| acl | test_acl_setfacl_default_group_acl | setfacl - set default group ACL on directory |
| acl | test_acl_setfacl_default_mask | setfacl - set default mask on directory |
| acl | test_acl_setfacl_default_other | setfacl - set default other on directory |
| acl | test_acl_setfacl_default_user_acl | setfacl - set default user ACL on directory |
| acl | test_acl_setfacl_export_and_restore | setfacl - export ACL and restore |
| acl | test_acl_setfacl_invalid_acl_type | setfacl - reject invalid ACL type tag |
| acl | test_acl_setfacl_invalid_perm_string | setfacl - reject invalid permission format |
| acl | test_acl_setfacl_invalid_permission | setfacl - reject invalid permission string |
| acl | test_acl_setfacl_modify_group_rx | setfacl -m set group r-x permission |
| acl | test_acl_setfacl_modify_mask_rwx | setfacl -m set mask to rwx |
| acl | test_acl_setfacl_modify_other_readonly | setfacl -m set other readonly |
| acl | test_acl_setfacl_modify_user_rwx | setfacl -m set user rwx permission |
| acl | test_acl_setfacl_multi_user_and_group | setfacl - set multiple user and group ACL entries |
| acl | test_acl_setfacl_nonexistent_file | setfacl - error on nonexistent file |
| acl | test_acl_setfacl_nonexistent_group | setfacl - reject nonexistent group |
| acl | test_acl_setfacl_nonexistent_user | setfacl - reject nonexistent user |
| acl | test_acl_setfacl_param_n_no_recalc_mask | setfacl -n do not recalculate mask |
| acl | test_acl_setfacl_permission_denied | setfacl - permission denied on protected file |
| acl | test_acl_setfacl_recursive_apply_to_subfile | setfacl -R apply ACL recursively to sub-files |
| acl | test_acl_setfacl_recursive_remove | setfacl -R -b recursively remove ACL |
| acl | test_acl_setfacl_recursive_set | setfacl -R recursively set ACL |
| acl | test_acl_setfacl_remove_all_acl | setfacl -b remove all extended ACL |
| acl | test_acl_setfacl_remove_default_acl | setfacl -k remove default ACL from directory |
| acl | test_acl_setfacl_remove_from_rules_file | setfacl -X remove ACL by rule file |
| acl | test_acl_setfacl_remove_group_entry | setfacl -x remove group ACL entry |
| acl | test_acl_setfacl_remove_user_entry | setfacl -x remove user ACL entry |
| acl | test_acl_setfacl_restore_dir_acl | setfacl --restore directory ACL from backup |
| acl | test_acl_setfacl_restore_file_acl | setfacl --restore file ACL from backup |
| acl | test_acl_setfacl_restore_from_rules_file | setfacl -M apply ACL from file |
| acl | test_acl_setfacl_set_named_user_acl | setfacl - set named user ACL entry |
| acl | test_acl_setfacl_set_replace_acl | setfacl --set replace entire ACL |
| acl | test_acl_setfacl_symlink_follow | setfacl -L follow symlink to set ACL |
| acl | test_acl_setfacl_symlink_nofollow | setfacl -P do not follow symlink |
| acl | test_acl_setfacl_test_dry_run | setfacl --test dry run does not modify ACL |
