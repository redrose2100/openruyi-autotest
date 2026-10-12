#!/bin/bash
# Functional test: flex - generated code options
. /usr/share/beakerlib/beakerlib.sh || exit 1

write_lex_l() {
    cat > "$TmpDir/lex.l" << 'LEXEOF'
%{
#include <stdio.h>
%}
%%
[0-9]+     printf("Matched number:%s\n",yytext);
.          /* ignore */
%%
LEXEOF
}

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y flex gcc 2>/dev/null
        write_lex_l
    rlPhaseEnd

    rlPhaseStartTest "flex --c++ (C++ mode)"
        rlRun "flex --c++ lex.l && test -f lex.yy.cc" 0 "flex --c++ generates C++ scanner"
    rlPhaseEnd

    rlPhaseStartTest "flex -D (define macro)"
        rlRun "flex -Dmacro lex.l && test -f lex.yy.c" 0 "flex -D defines preprocessor macro"
    rlPhaseEnd

    rlPhaseStartTest "flex -P (prefix)"
        rlRun "flex -PSTRING lex.l && test -f lex.STRING.c" 0 "flex -P changes prefix"
    rlPhaseEnd

    rlPhaseStartTest "flex -R (reentrant)"
        rlRun "flex -R lex.l && test -f lex.yy.c" 0 "flex -R generates reentrant scanner"
    rlPhaseEnd

    rlPhaseStartTest "flex --bison-bridge"
        rlRun "flex --bison-bridge lex.l && test -f lex.yy.c" 0 "flex --bison-bridge for bison compatibility"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd