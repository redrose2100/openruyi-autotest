# library-prefix = nettle

#

# nettle suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_nettle_suite"



nettleSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q nettle 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y nettle 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already nettle soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "nettle softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "nettle alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "nettleCleanup"

}



nettleCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y nettle 2>/dev/null || true

    rlLogInfo "already nettle soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "nettle Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
