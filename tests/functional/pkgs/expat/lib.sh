# library-prefix = expat

#

# expat suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_expat_suite"



expatSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q expat 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y expat 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already expat soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "expat softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "expat alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "expatCleanup"

}



expatCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y expat 2>/dev/null || true

    rlLogInfo "already expat soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "expat Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
