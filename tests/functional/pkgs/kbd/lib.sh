# library-prefix = kbd

#

# kbd suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_kbd_suite"



kbdSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q kbd 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y kbd 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already kbd soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "kbd softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "kbd alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "kbdCleanup"

}



kbdCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y kbd 2>/dev/null || true

    rlLogInfo "already kbd soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "kbd Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
