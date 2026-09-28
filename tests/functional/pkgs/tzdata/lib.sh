# library-prefix = tzdata

#

# tzdata suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_tzdata_suite"



tzdataSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q tzdata 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y tzdata 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already tzdata soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "tzdata softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "tzdata alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "tzdataCleanup"

}



tzdataCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y tzdata 2>/dev/null || true

    rlLogInfo "already tzdata soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "tzdata Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
