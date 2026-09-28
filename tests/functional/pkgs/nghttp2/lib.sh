# library-prefix = nghttp2

#

# nghttp2 suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_nghttp2_suite"



nghttp2Setup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q nghttp2 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y nghttp2 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already nghttp2 soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "nghttp2 softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "nghttp2 alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "nghttp2Cleanup"

}



nghttp2Cleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y nghttp2 2>/dev/null || true

    rlLogInfo "already nghttp2 soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "nghttp2 Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
