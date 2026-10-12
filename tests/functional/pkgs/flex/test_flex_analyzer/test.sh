#!/bin/bash
# Functional test: flex - analyzer table compression options
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

    rlPhaseStartTest "flex -Ca (align tables)"
        rlRun "flex -Ca lex.l && test -f lex.yy.c" 0 "flex -Ca generates aligned analyzer"
    rlPhaseEnd

    rlPhaseStartTest "flex -Ce (equivalence classes)"
        rlRun "flex -Ce lex.l && test -f lex.yy.c" 0 "flex -Ce uses equivalence classes"
    rlPhaseEnd

    rlPhaseStartTest "flex -Cf (full tables)"
        rlRun "flex -Cf lex.l && test -f lex.yy.c" 0 "flex -Cf generates full tables"
    rlPhaseEnd

    rlPhaseStartTest "flex -Cm (meta-EC)"
        rlRun "flex -Cm lex.l && test -f lex.yy.c" 0 "flex -Cm uses meta-EC"
    rlPhaseEnd

    rlPhaseStartTest "flex -Cr (read-only tables)"
        rlRun "flex -Cr lex.l && test -f lex.yy.c" 0 "flex -Cr uses read-only tables"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd