# library-prefix = libnetfilter_conntrack

#

# libnetfilter_conntrack suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_libnetfilter_conntrack_suite"



libnetfilterConntrackSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q libnetfilter_conntrack 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y libnetfilter_conntrack 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already libnetfilter_conntrack soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "libnetfilter_conntrack softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "libnetfilter_conntrack alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "libnetfilterConntrackCleanup"

}



libnetfilterConntrackCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y libnetfilter_conntrack 2>/dev/null || true

    rlLogInfo "already libnetfilter_conntrack soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "libnetfilter_conntrack Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
