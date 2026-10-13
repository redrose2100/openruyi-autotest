#!/bin/bash
# Functional test: flex - scanner behavior options
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

    rlPhaseStartTest "flex -7 (7-bit tables)"
        rlRun "flex -7 lex.l && test -f lex.yy.c" 0 "flex -7 generates 7-bit scanner"
    rlPhaseEnd

    rlPhaseStartTest "flex -8 (8-bit tables)"
        rlRun "flex -8 lex.l && test -f lex.yy.c" 0 "flex -8 generates 8-bit scanner"
    rlPhaseEnd

    rlPhaseStartTest "flex -B (batch)"
        rlRun "flex -B lex.l && test -f lex.yy.c" 0 "flex -B generates batch scanner"
    rlPhaseEnd

    rlPhaseStartTest "flex -i (case-insensitive)"
        rlRun "flex -i lex.l && test -f lex.yy.c" 0 "flex -i case-insensitive scanner"
    rlPhaseEnd

    rlPhaseStartTest "flex -l (maximum AT&T lex compatibility)"
        rlRun "flex -l lex.l && test -f lex.yy.c" 0 "flex -l max AT&T compat"
    rlPhaseEnd

    rlPhaseStartTest "flex --yylineno"
        rlRun "flex --yylineno lex.l && test -f lex.yy.c" 0 "flex --yylineno tracks line numbers"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd