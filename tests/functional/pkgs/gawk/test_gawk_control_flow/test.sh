#!/bin/bash
# Functional test: gawk - control flow: while, for, do-while, if/break
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        gawkSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        cat > scores.txt << 'EOF'
130 120 135
160 113 140
145 170 215
EOF
    rlPhaseEnd

    rlPhaseStartTest "gawk while loop average"
        rlRun "result=\$(gawk '{total=0; i=1; while(i<4){total += \$i; i++;}; avg=total/3; print \"Average:\",avg;}' scores.txt | head -1 | xargs); test \"\$result\" = 'Average: 128.333'" 0 "gawk while loop computes average"
    rlPhaseEnd

    rlPhaseStartTest "gawk while with if/break"
        rlRun "result=\$(gawk '{total=0; i=1; while(i<4){total += \$i; if(i == 2) break; i++;}; avg=total/2; print \"The average of the first two data elements is:\",avg;}' scores.txt | head -1 | xargs); test \"\$result\" = 'The average of the first two data elements is: 125'" 0 "gawk while/if/break combo"
    rlPhaseEnd

    rlPhaseStartTest "gawk do-while loop"
        rlRun "result=\$(gawk '{total=0; i=1; do {total += \$i; i++;} while(total <150); print total}' scores.txt | head -1); test \"\$result\" = '250'" 0 "gawk do-while loop"
    rlPhaseEnd

    rlPhaseStartTest "gawk for loop with printf"
        rlRun "result=\$(gawk '{total=0; for(i=1; i<4; i++){total += \$i;}; avg=total/3; printf \"Average: %5.1f\\n\",avg;}' scores.txt | head -1 | xargs); test \"\$result\" = 'Average: 128.3'" 0 "gawk for loop with printf formatting"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd