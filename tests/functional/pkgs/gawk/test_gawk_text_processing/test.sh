#!/bin/bash
# Functional test: gawk - text processing columns/substitutions/separators
. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        gawkSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        cat > data.txt << 'EOF'
hello world
goodbye world
nothing to do
EOF
        cat > data_csv.txt << 'EOF'
data11,data12,data13,data14,data15
data21,data22,data23,data24,data25
data31,data32,data33,data34,data35
EOF
        cat > data_multi.txt << 'EOF'
Rilly
123 Main Street
(312)555-1234

Frank
456 Oak Street
(317)555-9876

Haley
4231 Elm Street
(313)555-4938
EOF
    rlPhaseEnd

    rlPhaseStartTest "gawk print first column"
        rlRun "result=\$(gawk '{print \$1}' data.txt | xargs); test \"\$result\" = 'hello goodbye nothing'" 0 "gawk extracts first column"
    rlPhaseEnd

    rlPhaseStartTest "gawk gsub text replacement"
        rlRun "gawk '{gsub(/world/, \"orange\")} {print}' data.txt | grep -q orange" 0 "gawk gsub replaces text"
    rlPhaseEnd

    rlPhaseStartTest "gawk field editing"
        rlRun "result=\$(echo 'My name is Rich' | gawk '{\$4=\"Christine\"; print \$0}'); test \"\$result\" = 'My name is Christine'" 0 "gawk edits specific field"
    rlPhaseEnd

    rlPhaseStartTest "gawk BEGIN/END blocks"
        rlRun "gawk 'BEGIN {print \"The data File Contents:\"};{print \$0};END {print \"End of File\"}' data.txt | head -1 | grep -q 'File Contents'" 0 "gawk BEGIN block works"
    rlPhaseEnd

    rlPhaseStartTest "gawk FS field separator"
        rlRun "result=\$(gawk 'BEGIN{FS=\",\"} {print \$1,\$2,\$3}' data_csv.txt | head -1 | xargs); test \"\$result\" = 'data11 data12 data13'" 0 "gawk FS comma separator"
    rlPhaseEnd

    rlPhaseStartTest "gawk FS/OFS separator conversion"
        rlRun "result=\$(gawk 'BEGIN{FS=\",\"; OFS=\"-\"} {print \$1,\$2,\$3,\$4}' data_csv.txt | head -1); test \"\$result\" = 'data11-data12-data13-data14'" 0 "gawk FS/OFS conversion"
    rlPhaseEnd

    rlPhaseStartTest "gawk FS/RS multiline records"
        # RS="" makes blank-line-separated, FS="\n" makes each line a field
        rlRun "result=\$(gawk 'BEGIN{FS=\"\\n\"; RS=\"\"} {print \$1,\$3}' data_multi.txt | head -1 | xargs); test \"\$result\" = 'Rilly (312)555-1234'" 0 "gawk FS/RS multiline"
    rlPhaseEnd

    rlPhaseStartTest "gawk split function"
        rlRun "result=\$(gawk 'BEGIN{FS=\",\"} {split(\$0,var);print var[1],var[5]}' data_csv.txt | head -1 | xargs); test \"\$result\" = 'data11 data15'" 0 "gawk split function"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd