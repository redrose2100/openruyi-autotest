# library-prefix = systemd_timesyncd

#

# systemd-timesyncd suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_systemd_timesyncd_suite"



systemdTimesyncdSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q systemd-timesyncd 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y systemd-timesyncd 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already systemd-timesyncd soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "systemd-timesyncd softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "systemd-timesyncd alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "systemdTimesyncdCleanup"

}



systemdTimesyncdCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y systemd-timesyncd 2>/dev/null || true

    rlLogInfo "already systemd-timesyncd soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "systemd-timesyncd Retain (still have $ref test(s) not completed)"

    fi

}


# pkgs-full-test-run v1
