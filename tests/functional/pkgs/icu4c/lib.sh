# library-prefix = icu4c

#

# icu4c suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_icu4c_suite"



icu4cSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q icu4c 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y icu4c 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already icu4c soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "icu4c softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "icu4c alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "icu4cCleanup"

}



icu4cCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y icu4c 2>/dev/null || true

    rlLogInfo "already icu4c soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "icu4c Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
