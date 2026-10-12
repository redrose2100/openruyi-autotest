#!/bin/bash
# Functional test: gawk - built-in functions: FIELDWIDTHS, arrays, asort, string functions
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        gawkSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        cat > numbers.txt << 'EOF'
1005.3247596.37
11522.349194.00
05810.1298100.1
EOF
    rlPhaseEnd

    rlPhaseStartTest "gawk FIELDWIDTHS"
        rlRun "result=\$(gawk 'BEGIN{FIELDWIDTHS=\"3 5 2 5\"} {print \$1,\$2,\$3,\$4}' numbers.txt | head -1 | xargs); test \"\$result\" = '100 5.324 75 96.37'" 0 "gawk FIELDWIDTHS splits fixed-width fields"
    rlPhaseEnd

    rlPhaseStartTest "gawk variable arithmetic"
        rlRun "result=\$(gawk 'BEGIN{x = 4; x = x * 2 + 3; print x;}'); test \"\$result\" = '11'" 0 "gawk variable expression"
    rlPhaseEnd

    rlPhaseStartTest "gawk array operations"
        rlRun "result=\$(gawk 'BEGIN{var[1] = 34;var[2] = 3;total = var[1] + var[2];print total;}'); test \"\$result\" = '37'" 0 "gawk array sum"
    rlPhaseEnd

    rlPhaseStartTest "gawk toupper and length"
        rlRun "result=\$(gawk 'BEGIN{x=\"testing\"; print toupper(x),length(x)}'); test \"\$result\" = 'TESTING 7'" 0 "gawk toupper/length"
    rlPhaseEnd

    rlPhaseStartTest "gawk asort"
        rlRun "result=\$(gawk 'BEGIN{var[\"a\"]=5; var[\"g\"]=8; var[\"m\"]=6; var[\"u\"]=7; asort(var,test); for(i in test) print \"Index:\",i,\"- value\",test[i];}' | head -1 | xargs); test \"\$result\" = 'Index: 1 - value 5'" 0 "gawk asort sorts values"
    rlPhaseEnd

    rlPhaseStartTest "gawk asorti"
        rlRun "result=\$(gawk 'BEGIN{var[\"a\"]=5; var[\"g\"]=8; var[\"m\"]=6; var[\"u\"]=7; asorti(var,test); for(i in test) print \"Index:\",i,\"- value\",test[i];}' | head -1 | xargs); test \"\$result\" = 'Index: 1 - value a'" 0 "gawk asorti sorts indices"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd