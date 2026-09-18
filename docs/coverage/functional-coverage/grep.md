# grep 功能测试覆盖详情

共 **13** 个测试用例，**44** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| grep | test_grep_basic_pattern_matching | Basic grep for Hello |
| | | Verify multiple matches |
| | | Grep from pipe |
| | | Grep across multiple files |
| grep | test_grep_case_insensitive_i | Case insensitive grep |
| | | Verify case insensitive matches |
| | | Case sensitive: lowercase only matches lowercase |
| grep | test_grep_invert_match_v | Invert match: exclude Hello |
| | | Verify inverted output contains other lines |
| grep | test_grep_word_and_line_matching_w_x | Create word test file |
| | | Add line with separate words |
| | | Whole word match: hello matches only standalone |
| | | Create line test file |
| | | Add different line |
| | | Whole line exact match |
| grep | test_grep_count_and_line_numbers_c_n | Count matches with -c |
| | | Verify count >= 2 |
| | | Show line numbers with -n |
| | | Verify line number format |
| grep | test_grep_recursive_search_r | Recursive grep in subdirectory |
| | | Recursive list files with matches |
| | | Recursive with --include filter |
| grep | test_grep_extended_regex_e | Extended regex with alternation |
| | | Extended regex: digit quantifier |
| | | Verify digit match count |
| | | egrep equivalent to grep -E |
| grep | test_grep_fixed_strings_f | Fixed string with special chars |
| | | Fixed string: no regex meta-char interpretation |
| | | fgrep equivalent to grep -F |
| grep | test_grep_only_matching_and_quiet_o_q | Only matching: digits only |
| | | Quiet mode: pattern found |
| | | Quiet mode: pattern not found |
| grep | test_grep_context_lines_a_b_c | Context: 1 line after match |
| | | Context: 1 line before match |
| | | Context: 1 line before and after |
| grep | test_grep_file_listing_l_l | List files with matches |
| | | List files without matches |
| grep | test_grep_multiple_patterns_e_f | Multiple patterns with -e |
| | | Patterns from file with -f |
| | | Max count: stop after first match |
| grep | test_grep_error_handling | Error on nonexistent file |
| | | Error on invalid regex |
| | | Error on directory without -r |
| | | No match returns exit code 1 |
