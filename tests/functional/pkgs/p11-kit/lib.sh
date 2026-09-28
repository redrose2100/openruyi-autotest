# library-prefix = p11_kit

#

# p11-kit suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_p11_kit_suite"



p11KitSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q p11-kit 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y p11-kit 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already p11-kit soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "p11-kit softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "p11-kit alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "p11KitCleanup"

}



p11KitCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y p11-kit 2>/dev/null || true

    rlLogInfo "already p11-kit soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "p11-kit Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
