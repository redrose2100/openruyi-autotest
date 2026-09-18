# rpmbuild 功能测试覆盖详情

共 **9** 个测试套，**20** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_rpmbuild_rpmbuild_basic_functionality | 2 cases | Check rpmbuild version |
| | | Setup RPM build tree |
| test_rpmbuild_create_simple_spec_file | 1 cases | Create minimal spec file |
| test_rpmbuild_create_source_tarball | 2 cases | Create test source |
| | | Verify source file |
| test_rpmbuild_build_rpm_package | 2 cases | Build binary RPM |
| | | Build source RPM |
| test_rpmbuild_verify_built_rpm | 3 cases | Query RPM info |
| | | Verify RPM dependencies |
| | | Check RPM provides |
| test_rpmbuild_install_and_test_rpm | 3 cases | Install the RPM (test mode) |
| | | Actually install |
| | | Verify installation |
| test_rpmbuild_rpm_build_options | 2 cases | Build with --define |
| | | Check build log |
| test_rpmbuild_error_handling | 2 cases | Build with missing spec file |
| | | Build with missing source |
| test_rpmbuild_rpm_verification | 3 cases | Verify RPM signature (may not be signed) |
| | | Check RPM integrity |
| | | Cleanup |
