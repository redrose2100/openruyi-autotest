#!/bin/bash
# Functional test: flex - file output options
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

    rlPhaseStartTest "flex -o (output file)"
        rlRun "flex -o output.c lex.l && test -f output.c" 0 "flex -o writes to specified output"
    rlPhaseEnd

    rlPhaseStartTest "flex -t (stdout)"
        rlRun "flex -t lex.l | grep -q lex.yy.c" 0 "flex -t outputs to stdout"
    rlPhaseEnd

    rlPhaseStartTest "flex --header-file"
        rlRun "flex --header-file=lex.h lex.l && test -f lex.h" 0 "flex --header-file generates header"
    rlPhaseEnd

    rlPhaseStartTest "flex --tables-file"
        rlRun "flex --tables-file=tables.txt lex.l && test -f tables.txt" 0 "flex --tables-file generates tables"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd