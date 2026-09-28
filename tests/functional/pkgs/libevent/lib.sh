# library-prefix = libevent

#

# libevent suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_libevent_suite"



libeventSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q libevent 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y libevent 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already libevent soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "libevent softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "libevent alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "libeventCleanup"

}



libeventCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y libevent 2>/dev/null || true

    rlLogInfo "already libevent soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "libevent Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
