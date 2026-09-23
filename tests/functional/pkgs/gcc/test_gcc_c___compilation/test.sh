#!/bin/bash
# Functional test: gcc - C---compilation
# Beakerlib-based test with lifecycle management
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    gccSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
    rlRun "echo '#include <iostream>
int main() { std::cout << \"Hello C++\" << std::endl; return 0; }' > hello2.cpp" 0 "Create hello2.cpp"
    rlPhaseEnd

    rlPhaseStartTest "C---compilation"
    rlRun "g++ hello2.cpp -o hellocpp" 0 "Compile hello.cpp"
    rlRun "g++ -std=c++11 hello2.cpp -o hellocpp11" 0 "Compile with C++11 standard"
    rlPhaseEnd


    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    fi
    # gcc Package managed by lib.sh 's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
