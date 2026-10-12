#!/bin/bash
# Functional test: automake - autotools workflow
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        rlRun "mkdir main" 0 "Create source directory"
        rlRun "cd main" 0 "Enter source directory"
    rlPhaseEnd

    rlPhaseStartTest "autoscan - Generate configure.scan and autoscan.log"
        cat > main.c <<EOF
#include <stdio.h>
int main(int argc, char** argv)
{
    printf("Hello, Auto Makefile!\n");
    return 0;
}
EOF
        rlRun "autoscan" 0 "Run autoscan"
        rlRun "test -e autoscan.log" 0 "autoscan.log is generated"
        rlRun "test -e configure.scan" 0 "configure.scan is generated"
    rlPhaseEnd

    rlPhaseStartTest "aclocal - Generate aclocal.m4"
        mv configure.scan configure.in
        sed -i 's/^AC_INIT.*/AC_INIT([main],[1.0],[test@example.com])/g' configure.in
        sed -i 's/^AC_OUTPUT.*/AC_OUTPUT([Makefile])/g' configure.in
        sed -i '6i AM_INIT_AUTOMAKE([main],[1.0])' configure.in
        rlRun "aclocal" 0 "Run aclocal"
        rlRun "test -e aclocal.m4" 0 "aclocal.m4 is generated"
    rlPhaseEnd

    rlPhaseStartTest "autoconf - Generate configure script"
        rlRun "autoconf" 0 "Run autoconf"
        rlRun "test -e configure" 0 "configure is generated"
    rlPhaseEnd

    rlPhaseStartTest "autoheader - Generate config.h.in"
        rlRun "autoheader" 0 "Run autoheader"
        rlRun "test -e config.h.in" 0 "config.h.in is generated"
    rlPhaseEnd

    rlPhaseStartTest "automake - Generate Makefile.in with --add-missing"
        cat > Makefile.am <<EOF
AUTOMAKE_OPTIONS=foreign
bin_PROGRAMS=main
main_SOURCES=main.c
EOF
        rlRun "automake --add-missing" 0 "Run automake --add-missing"
    rlPhaseEnd

    rlPhaseStartTest "configure and make - Build the project"
        rlRun "./configure" 0 "Run configure"
        rlRun "make" 0 "Run make"
        rlRun "./main | grep 'Hello, Auto Makefile!'" 0 "main outputs expected message"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd