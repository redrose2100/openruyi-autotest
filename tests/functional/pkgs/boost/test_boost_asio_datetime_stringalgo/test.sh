#!/bin/bash
# Functional test: boost - asio, date_time, string_algo, optional and variant libraries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # The CI environment does not pre-install the packages listed in `require:`,
        # so install the compiler and the boost development files here. openRuyi
        # ships the linker symlinks in `boost` and the headers in `boost-devel`,
        # and its repository needs --nogpgcheck --setopt=sslverify=0.
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y \
            --nogpgcheck --setopt=sslverify=0 gcc-c++ boost boost-devel 2>&1 | tail -5
        rlRun "command -v g++" 0 "g++ is available"
        cat > boost_test.cpp <<'CPPEOF'
#include <iostream>
#include <string>
#include <vector>
#include <boost/asio.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/optional.hpp>
#include <boost/variant.hpp>

int main(int argc, char* argv[]) {
    if (argc < 2) { std::cout << "Usage: boost_test <module>\n"; return 1; }
    std::string module = argv[1];
    if (module == "asio") {
        boost::asio::io_context io;
        boost::asio::steady_timer timer(io, boost::asio::chrono::milliseconds(10));
        timer.async_wait([](const boost::system::error_code&) {});
        io.run();
        std::cout << "BOOST_ASIO_TIMER_OK\n";
        boost::asio::ip::tcp::socket sock(io);
        std::cout << "BOOST_ASIO_SOCKET_OK\n";
    }
    if (module == "date_time") {
        boost::gregorian::date d(2026, 7, 20);
        if (d.year() == 2026 && d.month() == 7 && d.day() == 20) std::cout << "BOOST_DATE_OK\n";
        boost::posix_time::ptime now = boost::posix_time::microsec_clock::local_time();
        std::cout << "BOOST_TIME_NOW_OK\n";
    }
    if (module == "string_algo") {
        std::string s = "  Hello Boost  ";
        boost::trim(s);
        if (s == "Hello Boost") std::cout << "BOOST_SA_TRIM_OK\n";
        std::vector<std::string> parts;
        boost::split(parts, s, boost::is_any_of(" "));
        if (parts.size() == 2) std::cout << "BOOST_SA_SPLIT_OK\n";
    }
    if (module == "optional") {
        boost::optional<int> opt;
        if (!opt) std::cout << "BOOST_OPT_EMPTY_OK\n";
        opt = 42;
        if (*opt == 42) std::cout << "BOOST_OPT_VALUE_OK\n";
    }
    if (module == "variant") {
        boost::variant<int, std::string> v(42);
        v = std::string("test");
        struct visitor : boost::static_visitor<void> {
            void operator()(int) const {}
            void operator()(const std::string&) const {}
        };
        boost::apply_visitor(visitor(), v);
        std::cout << "BOOST_VAR_VISITOR_OK\n";
    }
    return 0;
}
CPPEOF
    rlPhaseEnd

    rlPhaseStartTest "Compile and run asio test"
        # Boost.Asio only needs libstdc++/libpthread. Boost.System is header-only
        # since boost 1.87, so openRuyi ships no libboost_system.so to link with.
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_asio" 0 "Compile asio test"
        rlRun "./boost_test_asio asio | grep BOOST_ASIO_TIMER_OK" 0 "Asio timer works"
        rlRun "./boost_test_asio asio | grep BOOST_ASIO_SOCKET_OK" 0 "Asio socket works"
    rlPhaseEnd

    rlPhaseStartTest "Compile and run date_time test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_date_time -lboost_date_time" 0 "Compile date_time test"
        rlRun "./boost_test_date_time date_time | grep BOOST_DATE_OK" 0 "Date_time date works"
        rlRun "./boost_test_date_time date_time | grep BOOST_TIME_NOW_OK" 0 "Date_time time works"
    rlPhaseEnd

    rlPhaseStartTest "Compile and run string_algo test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_string_algo" 0 "Compile string_algo test"
        rlRun "./boost_test_string_algo string_algo | grep BOOST_SA_TRIM_OK" 0 "String_algo trim works"
        rlRun "./boost_test_string_algo string_algo | grep BOOST_SA_SPLIT_OK" 0 "String_algo split works"
    rlPhaseEnd

    rlPhaseStartTest "Compile and run optional/variant test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_other" 0 "Compile optional/variant test"
        rlRun "./boost_test_other optional | grep BOOST_OPT_VALUE_OK" 0 "Optional works"
        rlRun "./boost_test_other variant | grep BOOST_VAR_VISITOR_OK" 0 "Variant visitor works"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd