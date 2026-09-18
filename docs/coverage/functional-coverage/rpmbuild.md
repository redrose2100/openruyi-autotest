# rpmbuild 功能测试覆盖详情

共 **9** 个测试用例，**20** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| rpmbuild | test_rpmbuild_rpmbuild_basic_functionality | Check rpmbuild version |
| | | Setup RPM build tree |
| rpmbuild | test_rpmbuild_create_simple_spec_file | Create minimal spec file |
| rpmbuild | test_rpmbuild_create_source_tarball | Create test source |
| | | Verify source file |
| rpmbuild | test_rpmbuild_build_rpm_package | Build binary RPM |
| | | Build source RPM |
| rpmbuild | test_rpmbuild_verify_built_rpm | Query RPM info |
| | | Verify RPM dependencies |
| | | Check RPM provides |
| rpmbuild | test_rpmbuild_install_and_test_rpm | Install the RPM (test mode) |
| | | Actually install |
| | | Verify installation |
| rpmbuild | test_rpmbuild_rpm_build_options | Build with --define |
| | | Check build log |
| rpmbuild | test_rpmbuild_error_handling | Build with missing spec file |
| | | Build with missing source |
| rpmbuild | test_rpmbuild_rpm_verification | Verify RPM signature (may not be signed) |
| | | Check RPM integrity |
| | | Cleanup |
