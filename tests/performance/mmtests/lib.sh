# library-prefix = mmtests

#

# Kernel MMTests suite-level shared library

# Uses flag-file + reference counting for suite-level setup/cleanup.

#

# MMTests result determination (per documentation):

# - "test exit: <item> 0" → individual test item PASS

# - "test exit: <item> N" (N>0) → individual test item FAIL

# - No "test exit" markers + non-zero exit → FAIL

# - All "test exit" lines end with 0 → PASS

#

# Usage in each test file:

#. "$(dirname "$0")/../lib.sh" # from test_mmtests_*/ subdirectories



MMTESTS_DIR="/usr/libexec/MMTests"

MMTESTS_FLAG="/tmp/.beakerlib_mmtests_suite"



# Run a single MMTests config and check results.

# Pass / Fail mapping based on test exit markers.

# Usage: _mmtestsRunCase <config_name>

_mmtestsRunCase() {

    local config="$1"

    local out="/tmp/mmtests_out_$$"



    if [ ! -x "$MMTESTS_DIR/run-mmtests.sh" ]; then

    rlFail "MMTests runner not found ($MMTESTS_DIR/run-mmtests.sh)"

    return 1

    fi



    if [ ! -f "$MMTESTS_DIR/configs/$config" ]; then

    rlFail "MMTests config not found ($MMTESTS_DIR/configs/$config)"

    return 1

    fi



    cd "$MMTESTS_DIR" 2>/dev/null || true

    export AUTO_PACKAGE_INSTALL=yes

    # Pre-install common MMTests dependencies to avoid interactive prompts

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y procps-ng wget2 2>/dev/null || true

    # MMTests runs with sudo; pipe password for sudo, AUTO_PACKAGE_INSTALL handles dnf prompts

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | timeout --signal=KILL --kill-after=10 1800 \

    sudo -S -p "" bash run-mmtests.sh --no-monitor --config "configs/$config" "$config" 2>&1 | tee "$out"

    local rc=${PIPESTATUS[0]}



    # 1. Timeout

    if [ "$rc" -eq 137 ]; then

    rlFail "MMTests $config Executetimeout (by kill)"

    rm -f "$out"

    return 1

    fi



    # 2. Non-zero exit code

    if [ "$rc" -ne 0 ]; then

    rlFail "MMTests $config Execution failed (exit=$rc)"

    rm -f "$out"

    return 1

    fi



    # 3. Check for test exit markers

    local exit_lines

    exit_lines=$(grep '^test exit :: ' "$out" 2>/dev/null)

    if [ -z "$exit_lines" ]; then

    rlFail "MMTests $config resultnot (missing test exit)"

    rm -f "$out"

    return 1

    fi



    # 4. Check each test exit line -- all must end with 0

    local failed_items=""

    while IFS= read -r line; do

    local code

    code=$(echo "$line" | awk '{print $NF}')

    if [ "$code" != "0" ]; then

    local item

    item=$(echo "$line" | awk '{print $4}')

    failed_items="$failed_items $item"

    fi

    done <<< "$exit_lines"



    if [ -n "$failed_items" ]; then

    rlFail "MMTests $config testitemsfailed:$failed_items"

    rm -f "$out"

    return 1

    fi



    # 5. All test exit lines ended with 0 → PASS

    local item_count

    item_count=$(echo "$exit_lines" | wc -l)

    rlPass "MMTests $config testpassed ($item_count itemsallsuccess)"

    rm -f "$out"

    return 0

}



mmtestsSetup() {

    if [ ! -f "$MMTESTS_FLAG" ]; then

    if [ ! -x "$MMTESTS_DIR/run-mmtests.sh" ]; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y mmtests 2>/dev/null

    if [ ! -x "$MMTESTS_DIR/run-mmtests.sh" ]; then

    rlLogWarning "MMTests failed, test will be skipped"

    echo "installed=0" > "$MMTESTS_FLAG"

    else

    # Fix ownership so openruyi can write work/ and shellpacks/

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S chown -R openruyi:openruyi "$MMTESTS_DIR" 2>/dev/null

    echo "installed=1" > "$MMTESTS_FLAG"

    rlLogInfo "already MMTests ()"

    fi

    else

    echo "installed=0" > "$MMTESTS_FLAG"

    rlLogInfo "MMTests already exists"

    fi

    echo "ref=1" >> "$MMTESTS_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$MMTESTS_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$MMTESTS_FLAG"

    rlLogInfo "MMTests already, reference count: $ref"

    fi



    rlCleanupAppend "mmtestsCleanup"

}



mmtestsCleanup() {

    if [ ! -f "$MMTESTS_FLAG" ]; then return 0; fi

    local ref

    ref=$(grep "^ref=" "$MMTESTS_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    # Keep MMTests installed -- reinstall is too expensive (~8min + system updates)

    rm -f "$MMTESTS_FLAG"

    rlLogInfo "MMTests testCleanup complete (Retain)"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$MMTESTS_FLAG"

    rlLogInfo "MMTests Retain (still have $ref test(s) not completed)"

    fi

}