# library-prefix = blktests

#

# Kernel blktests suite-level shared library

# Uses flag-file + reference counting for suite-level setup/cleanup.

#

# blktests result determination:

# The check script outputs per-test results like:

# block/001 (test description) [passed]

# block/002 (test description) [not run]

# block/003 (test description) [failed]

# Pass if all tests are [passed] or [not run], no [failed].

#

# Usage in each test file:

#. "$(dirname "$0")/../lib.sh" # from test_blktests_*/ subdirectories



BLKTESTS_DIR="/usr/lib/blktests"

BLKTESTS_FLAG="/tmp/.beakerlib_blktests_suite"



# Run a single blktests test case.

# Usage: _blktestsRunCase <group> <test>

_blktestsRunCase() {

    local group="$1"

    local test="$2"

    local test_name="${group}/${test}"

    local out="/tmp/blktests_out_$$"



    if [ ! -x "$BLKTESTS_DIR/check" ]; then

    rlFail "blktests runner not found ($BLKTESTS_DIR/check)"

    return 1

    fi



    if [ ! -f "$BLKTESTS_DIR/tests/$group/$test" ]; then

    rlFail "blktests test not found ($BLKTESTS_DIR/tests/$group/$test)"

    return 1

    fi



    cd "$BLKTESTS_DIR" 2>/dev/null || true



    # blktests requires TEST_DEVS config; without devices, most tests will be [not run]

    # Create minimal config if it doesn't exist

    if [ ! -f "$BLKTESTS_DIR/config" ]; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S bash -c "cat > $BLKTESTS_DIR/config << 'EOF'

TIMEOUT=30

QUICK_RUN=1

EOF" 2>/dev/null || true

 echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S chown openruyi:openruyi "$BLKTESTS_DIR/config" 2>/dev/null || true

 fi



 timeout --signal=KILL --kill-after=10 600 \

 bash ./check "$test_name" 2>&1 | tee "$out"

 local rc=${PIPESTATUS[0]}



 # 1. Timeout

 if [ "$rc" -eq 137 ]; then

 rlFail "blktests $test_name Executetimeout"

 rm -f "$out"

 return 1

 fi



 # 2. Non-zero exit code

 if [ "$rc" -ne 0 ]; then

 rlFail "blktests $test_name Execution failed (exit=$rc)"

 rm -f "$out"

 return 1

 fi



 # 3. Check for explicit failure markers

 if grep -qE '\[failed\]' "$out"; then

 local failed

 failed=$(grep -E '\[failed\]' "$out" | head -3 | tr '\n' ' ')

 rlFail "blktests $test_name failed: $failed"

 rm -f "$out"

 return 1

 fi



 # 4. No failures found

 local status

 status=$(grep "$test_name" "$out" | grep -oE '\[(passed|not run|skipped)\]')

 rlPass "blktests $test_name $status"

 rm -f "$out"

 return 0

}



blktestsSetup() {

 if [ ! -f "$BLKTESTS_FLAG" ]; then

 if [ ! -x "$BLKTESTS_DIR/check" ]; then

 echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y blktests 2>/dev/null

 if [ ! -x "$BLKTESTS_DIR/check" ]; then

 rlLogWarning "blktests failed, test will be skipped"

 echo "installed=0" > "$BLKTESTS_FLAG"

 else

 echo "installed=1" > "$BLKTESTS_FLAG"

 rlLogInfo "already blktests ()"

 fi

 else

 echo "installed=0" > "$BLKTESTS_FLAG"

 rlLogInfo "blktests already exists"

 fi

 echo "ref=1" >> "$BLKTESTS_FLAG"

 else

 local ref

 ref=$(grep "^ref=" "$BLKTESTS_FLAG" | cut -d= -f2)

 ref=$((ref + 1))

 sed -i "s/^ref=.*/ref=$ref/" "$BLKTESTS_FLAG"

 rlLogInfo "blktests already, reference count: $ref"

 fi



 rlCleanupAppend "blktestsCleanup"

}



blktestsCleanup() {

 if [ ! -f "$BLKTESTS_FLAG" ]; then return 0; fi

 local ref

 ref=$(grep "^ref=" "$BLKTESTS_FLAG" | cut -d= -f2)

 ref=$((ref - 1))

 if [ "$ref" -le 0 ]; then

 rm -f "$BLKTESTS_FLAG"

 rlLogInfo "blktests testCleanup complete"

 else

 sed -i "s/^ref=.*/ref=$ref/" "$BLKTESTS_FLAG"

 rlLogInfo "blktests Retain (still have $ref test(s) not completed)"

 fi

}