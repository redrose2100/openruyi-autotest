# tar 功能测试覆盖详情

共 **10** 个测试用例，**27** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| tar | test_tar_basic_archive_creation | Create test files |
| | | Create tar archive |
| | | List archive contents |
| tar | test_tar_archive_extraction | Extract archive |
| | | Verify extracted files |
| tar | test_tar_compression_formats | Create gzip compressed archive |
| | | Create bzip2 compressed archive |
| | | Create xz compressed archive |
| | | Extract different formats |
| tar | test_tar_advanced_tar_options | Append files to existing archive |
| | | Extract specific files |
| | | Extract to different directory |
| | | Create archive from directory |
| tar | test_tar_archive_verification | Test archive integrity |
| | | Compare archive with original files |
| tar | test_tar_special_attributes | Preserve permissions |
| | | Preserve timestamps |
| tar | test_tar_error_handling | Non-existent file |
| | | Corrupted archive |
| | | Empty archive |
| tar | test_tar_wildcard_and_patterns | Extract with wildcard pattern |
| | | Exclude patterns |
| tar | test_tar_incremental_backup | Create incremental backup |
| | | Multi-volume archive (test only) |
| tar | test_tar_special_file_types | Archive with symlinks |
| | | Archive with hardlinks |
| | | Cleanup |
