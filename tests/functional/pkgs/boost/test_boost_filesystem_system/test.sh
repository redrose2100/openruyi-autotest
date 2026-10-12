#!/bin/bash
# Functional test: boost - filesystem and system libraries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        cat > boost_test.cpp <<'CPPEOF'
#include <iostream>
#include <string>
#include <boost/filesystem.hpp>
#include <boost/system/error_code.hpp>

int main(int argc, char* argv[]) {
    if (argc < 2) { std::cout << "Usage: boost_test <module>\n"; return 1; }
    std::string module = argv[1];
    if (module == "filesystem") {
        boost::filesystem::path p(".");
        if (boost::filesystem::exists(p)) std::cout << "BOOST_FS_EXISTS_OK\n";
        if (boost::filesystem::is_directory(p)) std::cout << "BOOST_FS_ISDIR_OK\n";
        boost::filesystem::path tmp = boost::filesystem::temp_directory_path();
        std::cout << "BOOST_FS_TEMP_OK\n";
        boost::filesystem::path abs = boost::filesystem::absolute(p);
        std::cout << "BOOST_FS_ABS_OK\n";
        std::string name = p.filename().string();
        std::cout << "BOOST_FS_FILENAME_OK\n";
    }
    if (module == "system") {
        boost::system::error_code ec;
        ec.assign(2, boost::system::generic_category());
        if (ec.value() == 2) std::cout << "BOOST_SYS_ERRCODE_OK\n";
        std::string msg = ec.message();
        std::cout << "BOOST_SYS_MSG_OK\n";
    }
    return 0;
}
CPPEOF
    rlPhaseEnd

    rlPhaseStartTest "Verify boost package installation"
        rpm -q boost
        rlRun "rpm -q boost | grep boost" 0 "boost package is installed"
        rlRun "rpm -V boost" 0 "boost package verification passed"
    rlPhaseEnd

    rlPhaseStartTest "Compile and run filesystem test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test -lboost_filesystem -lboost_system" 0 "Compile filesystem test"
        rlRun "./boost_test filesystem | grep BOOST_FS_EXISTS_OK" 0 "Filesystem exists() works"
        rlRun "./boost_test filesystem | grep BOOST_FS_ISDIR_OK" 0 "Filesystem is_directory() works"
        rlRun "./boost_test filesystem | grep BOOST_FS_TEMP_OK" 0 "Filesystem temp_directory_path() works"
        rlRun "./boost_test filesystem | grep BOOST_FS_ABS_OK" 0 "Filesystem absolute() works"
        rlRun "./boost_test filesystem | grep BOOST_FS_FILENAME_OK" 0 "Filesystem filename() works"
        rlRun "./boost_test system | grep BOOST_SYS_ERRCODE_OK" 0 "System error_code works"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd