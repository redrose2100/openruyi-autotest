#!/bin/bash
# ============================================================
# K8s suite-level shared library (Sonobuoy direct-evidence version)
# ============================================================
# Manages the sonobuoy CLI binary lifecycle across all K8s test
# cases using a flag-file + reference counting pattern:
#   - Installed ONCE (first test Setup) on the master node
#   - Verified via sha256sum + `sonobuoy version`
#   - Removed when reference count reaches 0 (last test Cleanup)
#
# NOTE (脚本直证性): this lib only handles the binary lifecycle and
# environment variables. Each test.sh MUST call sonobuoy CLI commands
# directly (sonobuoy run / retrieve / results / delete) in plain text.
#
# Usage in each test file:
#   . "$(dirname "$0")/../lib.sh"
#
# Then call: k8sLibSetup 1   in rlPhaseStartSetup
# Cleanup is auto-registered via rlCleanupAppend.
#
# Public functions:
#   k8sLibSetup <server_idx>        - ref count +1; install sonobuoy if first
#   k8sLibCleanup <server_idx>      - ref count -1; uninstall if last
#   k8sRunOnMaster <server_idx> <cmd...> - run command on master via hw_check
#   k8sGetSonobuoyImage <server_idx> - export SONOBUOY_IMAGE from containerd
# ============================================================

. /usr/share/beakerlib/beakerlib.sh || exit 1

# Flag file for reference counting (on the tmt runner machine)
K8S_FLAG="/tmp/.beakerlib_k8s_suite"

# Sonobuoy binary source (Nexus) and expected SHA256
SONOBUOY_VERSION="v0.57.3"
SONOBUOY_BIN_URL="https://nexus.osssc.ac.cn/repository/openruyi-k8s/v1.35.5/sonobuoy/bin/sonobuoy-${SONOBUOY_VERSION}-riscv64"
SONOBUOY_BIN_SHA256="0f5642a5ecbecc79e79aa3a1ab015c2e77d0027c51938fee7d5ac9d8dfd166be"
SONOBUOY_INSTALL_PATH="/usr/local/bin/sonobuoy"

# Kubeconfig on master node
K8S_KUBECONFIG="/etc/kubernetes/admin.conf"

# Source hw_check.sh for remote execution (resolves TEST_SERVER_* from topology.env)
_hw_lib="$(dirname "$0")/../../lib/hw_check.sh"
if [ -f "$_hw_lib" ]; then
    . "$_hw_lib"
fi

# ------------------------------------------------------------
# k8sRunOnMaster <server_idx> <cmd...>
#   Run a command on the master node (server idx), sudo injected.
#   This is only a transport wrapper -- sonobuoy logic lives in test.sh.
# ------------------------------------------------------------
k8sRunOnMaster() {
    local idx="$1"; shift
    hwRunOnServer "$idx" "sudo $*"
}

# ------------------------------------------------------------
# k8sGetSonobuoyImage <server_idx>
#   Probe containerd on the master for the pre-imported sonobuoy
#   image tag and export SONOBUOY_IMAGE.
# ------------------------------------------------------------
k8sGetSonobuoyImage() {
    local idx="$1"
    local img
    img=$(hwRunOnServer "$idx" "sudo ctr -n k8s.io images list | grep sonobuoy | awk '{print \$1}' | head -n1" 2>/dev/null)
    img=$(echo "$img" | tr -d '\r\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if [ -z "$img" ]; then
        img="localhost/sonobuoy/sonobuoy:${SONOBUOY_VERSION}"
    fi
    export SONOBUOY_IMAGE="$img"
    rlLogInfo "K8s: sonobuoy image = $SONOBUOY_IMAGE"
}

# ------------------------------------------------------------
# k8sInstallSonobuoy <server_idx>
#   Download + verify + install sonobuoy CLI on the master node.
# ------------------------------------------------------------
k8sInstallSonobuoy() {
    local idx="$1"

    rlLogInfo "K8s: installing sonobuoy $SONOBUOY_VERSION on master node..."

    # Download binary (retry up to 2 times)
    local attempt
    for attempt in 1 2; do
        hwRunOnServer "$idx" "curl -k -fL --retry 3 -o /tmp/sonobuoy-bin ${SONOBUOY_BIN_URL}"
        if [ $? -eq 0 ]; then
            break
        fi
        rlLogWarning "K8s: download attempt $attempt failed, retrying..."
        sleep 3
    done

    # Verify sha256
    local actual
    actual=$(hwRunOnServer "$idx" "sha256sum /tmp/sonobuoy-bin | awk '{print \$1}'" 2>/dev/null | tr -d '\r\n')
    if [ "$actual" != "$SONOBUOY_BIN_SHA256" ]; then
        rlFail "K8s: sonobuoy binary sha256 mismatch (got $actual, expected $SONOBUOY_BIN_SHA256)"
        hwRunOnServer "$idx" "rm -f /tmp/sonobuoy-bin"
        return 1
    fi

    # Install
    hwRunOnServer "$idx" "install -m 0755 /tmp/sonobuoy-bin ${SONOBUOY_INSTALL_PATH}"
    hwRunOnServer "$idx" "rm -f /tmp/sonobuoy-bin"

    # Verify CLI works
    hwRunOnServer "$idx" "sonobuoy version"
    if [ $? -ne 0 ]; then
        rlFail "K8s: sonobuoy version check failed after install"
        return 1
    fi

    rlLogInfo "K8s: sonobuoy installed successfully"
    return 0
}

# ------------------------------------------------------------
# k8sUninstallSonobuoy <server_idx>
#   Remove the sonobuoy CLI binary from the master node.
# ------------------------------------------------------------
k8sUninstallSonobuoy() {
    local idx="$1"
    rlLogInfo "K8s: uninstalling sonobuoy from master node..."
    hwRunOnServer "$idx" "rm -f ${SONOBUOY_INSTALL_PATH}"
}

# ------------------------------------------------------------
# k8sLibSetup <server_idx>
#   Call in rlPhaseStartSetup of every K8s test case.
# ------------------------------------------------------------
k8sLibSetup() {
    local idx="${1:-1}"

    if [ ! -f "$K8S_FLAG" ]; then
        # First test of the suite: install sonobuoy once
        echo "installed=0" > "$K8S_FLAG"
        echo "ref=1" >> "$K8S_FLAG"

        if k8sInstallSonobuoy "$idx"; then
            sed -i 's/^installed=.*/installed=1/' "$K8S_FLAG"
            k8sGetSonobuoyImage "$idx"
        else
            rlFail "K8s: sonobuoy installation failed, suite cannot run"
        fi
    else
        # Subsequent tests: increment ref count
        local ref
        ref=$(grep "^ref=" "$K8S_FLAG" | cut -d= -f2)
        ref=$((ref + 1))
        sed -i "s/^ref=.*/ref=$ref/" "$K8S_FLAG"
        rlLogInfo "K8s: suite already initialized by other tests, reference count: $ref"
    fi

    rlCleanupAppend "k8sLibCleanup $idx"
}

# ------------------------------------------------------------
# k8sLibCleanup <server_idx>
#   Auto-registered cleanup; decrements ref count and uninstalls
#   sonobuoy when the count reaches 0.
# ------------------------------------------------------------
k8sLibCleanup() {
    local idx="${1:-1}"

    if [ ! -f "$K8S_FLAG" ]; then
        return 0
    fi

    local ref
    ref=$(grep "^ref=" "$K8S_FLAG" | cut -d= -f2)
    ref=$((ref - 1))

    if [ "$ref" -le 0 ]; then
        k8sUninstallSonobuoy "$idx"
        rm -f "$K8S_FLAG"
        rlLogInfo "K8s: last test done, sonobuoy uninstalled and flag removed"
    else
        sed -i "s/^ref=.*/ref=$ref/" "$K8S_FLAG"
        rlLogInfo "K8s: cleanup retained (still $ref test(s) not completed)"
    fi
}
