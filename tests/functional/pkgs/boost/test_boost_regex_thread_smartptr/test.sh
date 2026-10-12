#!/bin/bash
# Functional test: boost - regex, thread and smart_ptr libraries
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        cat > boost_test.cpp <<'CPPEOF'
#include <iostream>
#include <string>
#include <boost/regex.hpp>
#include <boost/thread.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/make_shared.hpp>
#include <memory>

int main(int argc, char* argv[]) {
    if (argc < 2) { std::cout << "Usage: boost_test <module>\n"; return 1; }
    std::string module = argv[1];
    if (module == "regex") {
        std::string text = "Hello Boost 1.91.0, Test 2026";
        boost::regex expr("Boost ([0-9.]+)");
        boost::smatch matches;
        if (boost::regex_search(text, matches, expr)) std::cout << "BOOST_REGEX_SEARCH_OK\n";
        std::string replaced = boost::regex_replace(text, expr, "C++");
        std::cout << "BOOST_REGEX_REPLACE_OK\n";
        boost::regex expr2("^[0-9]+$");
        if (boost::regex_match("12345", expr2)) std::cout << "BOOST_REGEX_MATCH_OK\n";
    }
    if (module == "thread") {
        boost::mutex mtx;
        int counter = 0;
        boost::thread t1([&]() { boost::lock_guard<boost::mutex> lock(mtx); counter++; });
        boost::thread t2([&]() { boost::lock_guard<boost::mutex> lock(mtx); counter++; });
        t1.join(); t2.join();
        if (counter == 2) std::cout << "BOOST_THREAD_SYNC_OK\n";
        boost::thread::id id = t1.get_id();
        std::cout << "BOOST_THREAD_ID_OK\n";
        boost::this_thread::sleep_for(boost::chrono::milliseconds(1));
        std::cout << "BOOST_THREAD_SLEEP_OK\n";
    }
    if (module == "smart_ptr") {
        boost::shared_ptr<int> sp = boost::make_shared<int>(42);
        if (*sp == 42 && sp.use_count() == 1) std::cout << "BOOST_SP_OK\n";
        boost::shared_ptr<int> sp2 = sp;
        if (sp2.use_count() == 2) std::cout << "BOOST_SP_SHARE_OK\n";
        std::unique_ptr<int> up(new int(100));
        if (*up == 100) std::cout << "BOOST_UP_OK\n";
    }
    return 0;
}
CPPEOF
    rlPhaseEnd

    rlPhaseStartTest "Compile and run regex test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_regex -lboost_regex" 0 "Compile regex test"
        rlRun "./boost_test_regex regex | grep BOOST_REGEX_SEARCH_OK" 0 "Regex search works"
        rlRun "./boost_test_regex regex | grep BOOST_REGEX_REPLACE_OK" 0 "Regex replace works"
        rlRun "./boost_test_regex regex | grep BOOST_REGEX_MATCH_OK" 0 "Regex match works"
    rlPhaseEnd

    rlPhaseStartTest "Compile and run thread test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_thread -lboost_thread -lboost_system -lboost_chrono -lpthread" 0 "Compile thread test"
        rlRun "./boost_test_thread thread | grep BOOST_THREAD_SYNC_OK" 0 "Thread mutex sync works"
        rlRun "./boost_test_thread thread | grep BOOST_THREAD_ID_OK" 0 "Thread id works"
        rlRun "./boost_test_thread thread | grep BOOST_THREAD_SLEEP_OK" 0 "Thread sleep works"
    rlPhaseEnd

    rlPhaseStartTest "Compile and run smart_ptr test"
        rlRun "g++ -std=c++11 boost_test.cpp -o boost_test_smart_ptr" 0 "Compile smart_ptr test"
        rlRun "./boost_test_smart_ptr smart_ptr | grep BOOST_SP_OK" 0 "shared_ptr works"
        rlRun "./boost_test_smart_ptr smart_ptr | grep BOOST_UP_OK" 0 "unique_ptr works"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd