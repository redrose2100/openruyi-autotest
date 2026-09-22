# library-prefix = git

#

# git suite-level shared library

# Uses flag-file + reference counting to ensure the package

# is installed only ONCE and uninstalled only ONCE across all

# test cases.



PKG_FLAG="/tmp/.beakerlib_git_suite"



gitSetup() {

    if [ ! -f "$PKG_FLAG" ]; then

    if ! rpm -q git 2>/dev/null; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y git 2>/dev/null

    echo "installed=1" > "$PKG_FLAG"

    rlLogInfo "already git soft ()"

    else

    echo "installed=0" > "$PKG_FLAG"

    rlLogInfo "git softalready exists"

    fi

    echo "ref=1" >> "$PKG_FLAG"

    else

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref + 1))

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "git alreadybyothertest, reference count: $ref"

    fi

    rlCleanupAppend "gitCleanup"

    git config --global user.email "test@example.com" 2>/dev/null
    git config --global user.name "Test User" 2>/dev/null

}



gitCleanup() {

    if [ ! -f "$PKG_FLAG" ]; then

    return 0

    fi

    local ref

    ref=$(grep "^ref=" "$PKG_FLAG" | cut -d= -f2)

    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then

    if grep -q "^installed=1" "$PKG_FLAG"; then

    echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf remove -y git 2>/dev/null || true

    rlLogInfo "already git soft (posttest)"

    fi

    rm -f "$PKG_FLAG"

    else

    sed -i "s/^ref=.*/ref=$ref/" "$PKG_FLAG"

    rlLogInfo "git Retain (still have $ref test(s) not completed)"

    fi

}

