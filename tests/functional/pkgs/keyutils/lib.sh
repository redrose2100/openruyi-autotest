# library-prefix = keyutils

#

# keyutils suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_keyutils_suite"



keyutilsSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q keyutils 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y keyutils 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already keyutils soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "keyutils softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "keyutils alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "keyutilsCleanup"

}



keyutilsCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y keyutils 2>/dev/null || true

    rlLogInfo "already keyutils soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "keyutils Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
