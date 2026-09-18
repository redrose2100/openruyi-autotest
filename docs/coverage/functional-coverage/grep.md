# grep 功能测试覆盖详情

共 **13** 个测试套，**44** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_grep_basic_pattern_matching | 4 cases | Basic grep for Hello |
| | | Verify multiple matches |
| | | Grep from pipe |
| | | Grep across multiple files |
| test_grep_case_insensitive_i | 3 cases | Case insensitive grep |
| | | Verify case insensitive matches |
| | | Case sensitive: lowercase only matches lowercase |
| test_grep_invert_match_v | 2 cases | Invert match: exclude Hello |
| | | Verify inverted output contains other lines |
| test_grep_word_and_line_matching_w_x | 6 cases | Create word test file |
| | | Add line with separate words |
| | | Whole word match: hello matches only standalone |
| | | Create line test file |
| | | Add different line |
| | | Whole line exact match |
| test_grep_count_and_line_numbers_c_n | 4 cases | Count matches with -c |
| | | Verify count >= 2 |
| | | Show line numbers with -n |
| | | Verify line number format |
| test_grep_recursive_search_r | 3 cases | Recursive grep in subdirectory |
| | | Recursive list files with matches |
| | | Recursive with --include filter |
| test_grep_extended_regex_e | 4 cases | Extended regex with alternation |
| | | Extended regex: digit quantifier |
| | | Verify digit match count |
| | | egrep equivalent to grep -E |
| test_grep_fixed_strings_f | 3 cases | Fixed string with special chars |
| | | Fixed string: no regex meta-char interpretation |
| | | fgrep equivalent to grep -F |
| test_grep_only_matching_and_quiet_o_q | 3 cases | Only matching: digits only |
| | | Quiet mode: pattern found |
| | | Quiet mode: pattern not found |
| test_grep_context_lines_a_b_c | 3 cases | Context: 1 line after match |
| | | Context: 1 line before match |
| | | Context: 1 line before and after |
| test_grep_file_listing_l_l | 2 cases | List files with matches |
| | | List files without matches |
| test_grep_multiple_patterns_e_f | 3 cases | Multiple patterns with -e |
| | | Patterns from file with -f |
| | | Max count: stop after first match |
| test_grep_error_handling | 4 cases | Error on nonexistent file |
| | | Error on invalid regex |
| | | Error on directory without -r |
| | | No match returns exit code 1 |
