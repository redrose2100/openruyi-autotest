# ed Functional Test Coverage Details

**27** test cases in total, **27** test points

| Package | Test Case | Test Point |
|---------|-----------|------------|
| ed | test_ed_address_dollar | Address the last line with $ |
| ed | test_ed_address_range | Address a range of lines with start,end |
| ed | test_ed_address_regex | Address lines by regex pattern /pattern/ |
| ed | test_ed_address_relative | Use relative addressing with + and - |
| ed | test_ed_basic_append_print | Append text to buffer and print it |
| ed | test_ed_basic_change_line | Change a line with c command |
| ed | test_ed_basic_delete | Delete a specific line with d command |
| ed | test_ed_basic_insert | Insert text before current line with i command |
| ed | test_ed_basic_open_quit | Open file and quit without modification |
| ed | test_ed_basic_write | Create and write to file with ed |
| ed | test_ed_copy_lines | Copy lines with t (transfer) command |
| ed | test_ed_error_invalid_command | Handle invalid command gracefully |
| ed | test_ed_error_nonexistent_file | Handle error when opening nonexistent file |
| ed | test_ed_global_command | Apply command to matching lines with g/ |
| ed | test_ed_global_inverse | Apply command to non-matching lines with v/ |
| ed | test_ed_join_lines | Join adjacent lines with j command |
| ed | test_ed_mark_lines | Mark a line and address it by mark name |
| ed | test_ed_move_lines | Move lines to new position with m |
| ed | test_ed_prompt_mode | Set custom prompt string with -p |
| ed | test_ed_read_file | Read and insert content from external file |
| ed | test_ed_script_mode | Run ed in silent/script mode with -s |
| ed | test_ed_substitute_basic | Basic text substitution on a line |
| ed | test_ed_substitute_delimiter | Use custom delimiter in substitution |
| ed | test_ed_substitute_global | Global substitution replaces all occurrences |
| ed | test_ed_substitute_regex | Use regex and backreference in substitution |
| ed | test_ed_undo | Undo the last modification with u |
| ed | test_ed_write_range | Write specific line range to another file |
