# rpmbuild Functional Test Coverage Details

**18** test cases in total, **18** test points

| Package | Test Case | Test Point |
|---------|-----------|------------|
| rpmbuild | test_rpmbuild_ba | rpmbuild -ba build all |
| rpmbuild | test_rpmbuild_bb | rpmbuild -bb build binary |
| rpmbuild | test_rpmbuild_bc | rpmbuild -bc compile only |
| rpmbuild | test_rpmbuild_bi | rpmbuild -bi install only |
| rpmbuild | test_rpmbuild_bl | rpmbuild -bl list files |
| rpmbuild | test_rpmbuild_bp | rpmbuild -bp prep only |
| rpmbuild | test_rpmbuild_bs | rpmbuild -bs build source |
| rpmbuild | test_rpmbuild_build_rpm_package | Build-RPM-package |
| rpmbuild | test_rpmbuild_clean | rpmbuild --clean clean after |
| rpmbuild | test_rpmbuild_create_simple_spec_file | Create-simple-spec-file |
| rpmbuild | test_rpmbuild_create_source_tarball | Create-source-tarball |
| rpmbuild | test_rpmbuild_define | rpmbuild --define macro |
| rpmbuild | test_rpmbuild_error_handling | Error-handling |
| rpmbuild | test_rpmbuild_install_and_test_rpm | Install-and-test-RPM |
| rpmbuild | test_rpmbuild_nocheck | rpmbuild --nocheck skip tests |
| rpmbuild | test_rpmbuild_rmsource | rpmbuild --rmsource |
| rpmbuild | test_rpmbuild_rpmbuild_basic_functionality | rpmbuild-basic-functionality |
| rpmbuild | test_rpmbuild_verify_built_rpm | Verify-built-RPM |
