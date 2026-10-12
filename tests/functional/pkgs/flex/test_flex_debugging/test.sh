#!/bin/bash
# Functional test: flex - debugging options
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

    rlPhaseStartTest "flex -d (debug mode)"
        rlRun "flex -d lex.l && test -f lex.yy.c" 0 "flex -d enables debug output"
    rlPhaseEnd

    rlPhaseStartTest "flex -b (backup info)"
        rlRun "flex -b lex.l && test -f lex.backup" 0 "flex -b generates lex.backup"
    rlPhaseEnd

    rlPhaseStartTest "flex -T (trace)"
        rlRun "flex -T lex.l && test -f lex.yy.c" 0 "flex -T enables trace"
    rlPhaseEnd

    rlPhaseStartTest "flex -w (suppress warnings)"
        rlRun "flex -w lex.l && test -f lex.yy.c" 0 "flex -w suppresses warnings"
    rlPhaseEnd

    rlPhaseStartTest "flex -v (verbose)"
        rlRun "flex -v lex.l && test -f lex.yy.c" 0 "flex -v verbose mode"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd