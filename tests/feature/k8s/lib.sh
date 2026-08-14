# library-prefix = k8s

#

# K8s suite-level shared library

# Provides sonobuoy CLI installation/removal with reference counting,

# and smoke plugin manifest download.

#

# All functions run LOCALLY on the K8s master node (tmt provision: local).

# No SSH remote invocation is involved.

#

# Sonobuoy facts (verified):
#   - CLI:     sonobuoy-v0.57.3-riscv64, SHA256 0f5642a5ecbecc79e79aa3a1ab015c2e77d0027c51938fee7d5ac9d8dfd166be
#   - Source:  https://nexus.osssc.ac.cn/repository/openruyi-k8s/v1.35.5/sonobuoy/bin/sonobuoy-v0.57.3-riscv64
#   - Smoke plugin manifest:
#              https://nexus.osssc.ac.cn/repository/openruyi-k8s/v1.35.5/manifests/openruyi-riscv-sonobuoy-smoke.yaml
#
# Usage:
#   . "$(dirname "$0")/../lib.sh"   # from cluster_ready/ or sonobuoy_smoke/
#   k8sLibSetup                      # in Setup phase
#   k8sFetchSmokePlugin              # fetch plugin manifest to /tmp
#   k8sLibCleanup                    # registered via rlCleanupAppend

K8S_FLAG="/tmp/.beakerlib_k8s_suite"

SONOBUOY_VERSION="v0.57.3"
SONOBUOY_BIN="sonobuoy-${SONOBUOY_VERSION}-riscv64"
SONOBUOY_INSTALL="/usr/local/bin/sonobuoy"
SONOBUOY_SHA256="0f5642a5ecbecc79e79aa3a1ab015c2e77d0027c51938fee7d5ac9d8dfd166be"
SONOBUOY_URL="https://nexus.osssc.ac.cn/repository/openruyi-k8s/v1.35.5/sonobuoy/bin/${SONOBUOY_BIN}"

K8S_SMOKE_PLUGIN="/tmp/openruyi-riscv-sonobuoy-smoke.yaml"
K8S_SMOKE_PLUGIN_URL="https://nexus.osssc.ac.cn/repository/openruyi-k8s/v1.35.5/manifests/openruyi-riscv-sonobuoy-smoke.yaml"

K8S_KUBECONFIG="/etc/kubernetes/admin.conf"



# Download sonobuoy CLI, verify SHA256, install to /usr/local/bin.
# Returns 0 on success, 1 on failure (after retries).
_k8sInstallSonobuoy() {
    local attempts=0
    while [ "$attempts" -lt 2 ]; do
        attempts=$((attempts + 1))
        rlLogInfo "Downloading sonobuoy (attempt $attempts/2): $SONOBUOY_URL"
        if rlRun "curl -fsSL -o /tmp/$SONOBUOY_BIN '$SONOBUOY_URL'" 0 "Download sonobuoy"; then
            break
        fi
    done
    if [ ! -f "/tmp/$SONOBUOY_BIN" ]; then
        rlFail "Sonobuoy download failed after retries"
        return 1
    fi

    # Verify SHA256
    local actual
    actual=$(sha256sum "/tmp/$SONOBUOY_BIN" | awk '{print $1}')
    if [ "$actual" != "$SONOBUOY_SHA256" ]; then
        rlLogWarning "SHA256 mismatch (got $actual), re-downloading once"
        rm -f "/tmp/$SONOBUOY_BIN"
        rlRun "curl -fsSL -o /tmp/$SONOBUOY_BIN '$SONOBUOY_URL'" 0 "Re-download sonobuoy"
        actual=$(sha256sum "/tmp/$SONOBUOY_BIN" | awk '{print $1}')
        if [ "$actual" != "$SONOBUOY_SHA256" ]; then
            rlFail "Sonobuoy SHA256 verification failed"
            rm -f "/tmp/$SONOBUOY_BIN"
            return 1
        fi
    fi

    rlRun "install -m 0755 /tmp/$SONOBUOY_BIN '$SONOBUOY_INSTALL'" 0 "Install sonobuoy to /usr/local/bin"
    rm -f "/tmp/$SONOBUOY_BIN"
    return 0
}



# Download the official smoke plugin manifest to /tmp.
# Returns 0 on success, 1 on failure.
k8sFetchSmokePlugin() {
    rlRun "curl -fsSL -o '$K8S_SMOKE_PLUGIN' '$K8S_SMOKE_PLUGIN_URL'" 0 "Download smoke plugin manifest"
    if [ ! -s "$K8S_SMOKE_PLUGIN" ]; then
        rlFail "Smoke plugin manifest is empty or missing"
        return 1
    fi
    rlLogInfo "Smoke plugin manifest ready: $K8S_SMOKE_PLUGIN"
    return 0
}



# Suite-level setup with reference counting.
# Install sonobuoy only once across all cases; register cleanup.
k8sLibSetup() {
    if [ ! -f "$K8S_FLAG" ]; then
        # First case in suite: install sonobuoy
        if ! _k8sInstallSonobuoy; then
            rlFail "Sonobuoy installation failed (setup FAIL, case SKIP)"
            return 1
        fi
        rlRun "sonobuoy version" 0 "Verify sonobuoy CLI"
        echo "ref=1" > "$K8S_FLAG"
    else
        local ref
        ref=$(grep "^ref=" "$K8S_FLAG" | cut -d= -f2)
        ref=$((ref + 1))
        sed -i "s/^ref=.*/ref=$ref/" "$K8S_FLAG"
    fi

    rlCleanupAppend "k8sLibCleanup"
    return 0
}



# Suite-level cleanup with reference counting.
# Remove sonobuoy only when the last case finishes.
k8sLibCleanup() {
    if [ ! -f "$K8S_FLAG" ]; then return 0; fi
    local ref
    ref=$(grep "^ref=" "$K8S_FLAG" | cut -d= -f2)
    ref=$((ref - 1))
    if [ "$ref" -le 0 ]; then
        rm -f "$K8S_FLAG"
        rlRun "rm -f '$SONOBUOY_INSTALL'" 0 "Remove sonobuoy binary"
        rlLogInfo "K8s suite cleanup complete"
    else
        sed -i "s/^ref=.*/ref=$ref/" "$K8S_FLAG"
        rlLogInfo "K8s suite retained (still have $ref test(s) not completed)"
    fi
}
