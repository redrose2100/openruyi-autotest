# coreutils 功能测试覆盖详情

共 **24** 个测试套，**234** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_coreutils_file_creation_and_listing_echo_cat_ls_dir_vdir | 15 cases | echo create file |
| | | echo append |
| | | echo -n suppress newline |
| | | echo -n: verify no trailing newline |
| | | cat display file |
| | | cat: verify 2 lines |
| | | cat -n number all lines |
| | | cat -b number non-blank lines |
| | | ls -la list all files |
| | | ls specific file |
| | | ls -l: regular file check |
| | | ls -ld: directory check |
| | | ls -1 single column |
| | | dir list directory |
| | | vdir long format list |
| test_coreutils_copy_move_remove_cp_mv_rm_rmdir | 18 cases | cp copy file |
| | | cp: verify copy exists |
| | | cp: files identical |
| | | cp -r recursive copy |
| | | cp -r: verify directory copy |
| | | mv rename file |
| | | mv: old name gone |
| | | mv: new name exists |
| | | mv to subdirectory |
| | | Create temp file |
| | | rm remove file |
| | | rm: file removed |
| | | Create dir to remove |
| | | rm -rf recursive force |
| | | rm -rf: directory removed |
| | | Create empty directory |
| | | rmdir remove empty directory |
| | | rmdir: directory removed |
| test_coreutils_directory_file_creation_temp_files_mkdir_touch_mktemp | 7 cases | mkdir -p nested directories |
| | | mkdir -p: verify nested dir |
| | | mkdir -m set mode |
| | | touch create file |
| | | touch: file exists |
| | | touch -t set timestamp |
| | | touch -a access time only |
| test_coreutils_links_and_path_resolution_ln_link_unlink_readlink_realpath | 15 cases | Create link source |
| | | ln create hard link |
| | | ln: hard link same inode |
| | | ln -s symbolic link |
| | | ln -s: symlink exists |
| | | ln -s: read through symlink |
| | | ln -sf force recreate symlink |
| | | link create hard link |
| | | link: same inode |
| | | unlink remove hard link |
| | | unlink: file removed |
| | | readlink show symlink target |
| | | readlink: correct target |
| | | readlink -f canonicalize |
| | | realpath canonical path |
| test_coreutils_file_viewing_head_tail_tac_nl | 10 cases | head -n 5: first 5 lines |
| | | head -n 3: verify count |
| | | head -c 10: first 10 bytes |
| | | tail -n 5: last 5 lines |
| | | tail -n 3: verify count |
| | | tail -n +18: from line 18 |
| | | tail -c 10: last 10 bytes |
| | | tac reverse lines |
| | | tac: first becomes last |
| | | nl number lines |
| test_coreutils_counting_and_statistics_wc_du_df_stat | 12 cases | wc -l line count |
| | | wc -l: 20 lines |
| | | wc -c byte count |
| | | wc -w word count |
| | | wc -m character count |
| | | du -sh summary human |
| | | du -h directory usage |
| | | df -h human readable |
| | | df: root filesystem |
| | | stat file status |
| | | stat -c format output |
| | | stat -f filesystem status |
| test_coreutils_text_processing_i_sort_uniq_cut_tr | 17 cases | sort alphabetically |
| | | sort: first is apple |
| | | sort -r reverse |
| | | sort -u unique |
| | | sort -n numeric |
| | | uniq unique lines |
| | | uniq: 4 unique |
| | | uniq -c count occurrences |
| | | uniq -d only duplicates |
| | | uniq -u only uniques |
| | | cut -d: -f1 first field |
| | | cut -d: -f2 second field |
| | | cut multiple fields |
| | | cut -c character range |
| | | tr translate uppercase to lowercase |
| | | tr -d delete characters |
| | | tr -s squeeze repeats |
| test_coreutils_text_processing_ii_paste_comm_join_fmt_fold_pr_expand_unexpand | 12 cases | paste merge files side by side |
| | | paste -d: custom delimiter |
| | | paste -s serial |
| | | comm compare sorted files |
| | | join files on common field |
| | | fmt reformat text |
| | | fmt -w set width |
| | | fold -w wrap at width |
| | | pr paginate file |
| | | pr -n number lines |
| | | expand tabs to spaces |
| | | unexpand -a spaces to tabs |
| test_coreutils_octal_dump_od | 4 cases | od octal dump |
| | | od -c character dump |
| | | od -x hex dump |
| | | od -A x hex address |
| test_coreutils_path_operations_basename_dirname_pwd | 5 cases | basename extract filename |
| | | basename strip suffix |
| | | dirname extract directory |
| | | dirname path extraction |
| | | pwd print working directory |
| test_coreutils_permissions_and_ownership_chmod_chown_chgrp | 10 cases | Create permission test file |
| | | chmod u+x add exec |
| | | chmod: verify exec set |
| | | chmod 644 numeric |
| | | chmod: verify 644 perms |
| | | Setup recursive chmod |
| | | chmod -R recursive |
| | | chown version check |
| | | chown to self |
| | | chgrp version check |
| test_coreutils_redirection_tee | 3 cases | tee write to file |
| | | tee: verify output |
| | | tee -a append mode |
| test_coreutils_checksums_cksum_md5sum_sha1sum_sha224sum_sha384sum_sha512sum_sha256sum_b2sum_sum | 15 cases | cksum CRC checksum |
| | | md5sum compute |
| | | md5sum save |
| | | md5sum -c verify |
| | | sha1sum compute |
| | | sha1sum save |
| | | sha1sum -c verify |
| | | sha224sum compute |
| | | sha256sum compute |
| | | sha256sum save |
| | | sha256sum -c verify |
| | | sha384sum compute |
| | | sha512sum compute |
| | | b2sum BLAKE2 checksum |
| | | sum BSD checksum |
| test_coreutils_encoding_base32_base64_basenc | 5 cases | base32 encode |
| | | base32 -d decode |
| | | base64 encode |
| | | base64 -d decode |
| | | basenc --base64 encode |
| test_coreutils_system_information_uname_who_whoami_id_groups_users_hostid_nproc_tty_logname_pinky | 18 cases | uname system name |
| | | uname -a all info |
| | | uname -r kernel release |
| | | uname -m machine hardware |
| | | who show logged in users |
| | | whoami current user |
| | | id user identity |
| | | id -u user ID |
| | | id -g group ID |
| | | groups show group membership |
| | | groups for specific user |
| | | users list logged in users |
| | | hostid numeric host identifier |
| | | nproc number of CPUs |
| | | nproc --all all processors |
| | | tty terminal name |
| | | logname login name |
| | | pinky user info |
| test_coreutils_boolean_and_condition_true_false_test | 8 cases | true returns success |
| | | false returns failure |
| | | test -f: file exists |
| | | test -d: directory exists |
| | | test string equality |
| | | test numeric comparison |
| | | [ -f: file exists |
| | | [ string equality |
| test_coreutils_environment_and_time_env_printenv_date_printf | 8 cases | env show environment |
| | | env set variable for command |
| | | printenv show PATH |
| | | date current date/time |
| | | date custom format |
| | | date -u UTC time |
| | | printf formatted output |
| | | printf string output |
| test_coreutils_flow_control_sleep_timeout_yes | 6 cases | sleep delay |
| | | timeout: command finishes in time |
| | | timeout: successful completion |
| | | timeout: kills slow command |
| | | yes repeated output |
| | | yes custom string |
| test_coreutils_process_control_nice_nohup_stdbuf | 3 cases | nice adjust priority |
| | | nohup run command |
| | | stdbuf line buffered output |
| test_coreutils_file_operations_dd_truncate_shred_sync_install_chroot | 15 cases | dd copy file |
| | | truncate set size |
| | | truncate: verify size |
| | | Create file to shred |
| | | shred remove file securely |
| | | shred: file removed |
| | | sync flush filesystem buffers |
| | | install copy with mode |
| | | install: destination exists |
| | | install -d create directory |
| | | install -d: directory exists |
| | | chroot version check |
| | | mkfifo create named pipe |
| | | mkfifo: verify pipe created |
| | | mknod version check |
| test_coreutils_numbers_and_expressions_seq_factor_shuf_numfmt_expr | 13 cases | seq generate sequence |
| | | seq: 5 numbers |
| | | seq -s custom separator |
| | | factor prime factorization |
| | | factor prime number |
| | | shuf randomize lines |
| | | shuf: same line count |
| | | numfmt to SI units |
| | | numfmt from SI units |
| | | numfmt to IEC units |
| | | expr basic arithmetic |
| | | expr multiplication |
| | | expr string length |
| test_coreutils_split_files_split_csplit | 3 cases | split by lines |
| | | split: multiple output files |
| | | csplit split by pattern |
| test_coreutils_special_utilities_stty_pathchk_tsort_ptx_dircolors | 7 cases | stty -a show all terminal settings |
| | | pathchk validate path |
| | | pathchk -p POSIX check |
| | | tsort topological sort |
| | | ptx permuted index |
| | | dircolors -p print database |
| | | dircolors output LS_COLORS |
| test_coreutils_error_handling | 5 cases | cp: error on nonexistent source |
| | | ls: error on nonexistent file |
| | | mkdir: error on existing dir |
| | | rm: error on dir without -r |
| | | rmdir: error on non-empty dir |
