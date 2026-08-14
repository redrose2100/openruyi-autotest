#!/bin/bash
# K8s feature test: sonobuoy smoke
# Run the official openruyi-riscv sonobuoy smoke plugin against the cluster:
#   sonobuoy delete -> run -> retrieve -> results (full closed loop)
# Expect: Total: 2, Passed: 2, Failed: 0, every node status: passed
#
# Runs LOCALLY on the K8s master node (tmt provision: local).
# Sonobuoy CLI calls are written out explicitly (no hidden wrappers).

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

SONOBUOY_CMD="/usr/local/bin/sonobuoy"
KUBECONFIG="/etc/kubernetes/admin.conf"
SMOKE_PLUGIN="/tmp/openruyi-riscv-sonobuoy-smoke.yaml"
RESULTS_DIR="/tmp"
RESULTS_TAR="$RESULTS_DIR/k8s-smoke-results.tar.gz"
RESULTS_LOG="$RESULTS_DIR/k8s-smoke-results.txt"
SONOBUOY_IMAGE="localhost/sonobuoy/sonobuoy:v0.57.3-riscv64"

EXPECT_TOTAL=2
EXPECT_PASSED=2
EXPECT_FAILED=0

# Add sudo prefix when not running as root (kubeconfig + /usr/local/bin are root-owned)
SUDO_PREFIX=""
if [ "$(id -u)" -ne 0 ]; then
    SUDO_PREFIX="sudo -n"
fi

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        k8sLibSetup
        k8sFetchSmokePlugin
        rlRun "kubectl --kubeconfig=$KUBECONFIG get nodes" 0 "List cluster nodes"
        rlRun "cd $RESULTS_DIR" 0 "Enter results directory"
        rlPhaseEnd

    rlPhaseStartTest "Sonobuoy smoke test (full loop)"
        # 1. Clean any leftovers from previous runs
        rlRun "$SUDO_PREFIX $SONOBUOY_CMD delete --wait --kubeconfig=$KUBECONFIG || true" 0 "Clean previous sonobuoy resources"

        # 2. Run the smoke plugin (DaemonSet, one pod per node), wait for completion
        rlRun "$SUDO_PREFIX $SONOBUOY_CMD run \
            --sonobuoy-image $SONOBUOY_IMAGE \
            --plugin $SMOKE_PLUGIN \
            --image-pull-policy Never \
            --wait \
            --kubeconfig=$KUBECONFIG" 0 "Run sonobuoy smoke plugin (--wait)"

        # 3. Retrieve results archive (note: -f name is saved under CWD, so cd to /tmp first)
        rlRun "$SUDO_PREFIX $SONOBUOY_CMD retrieve -f $(basename $RESULTS_TAR) --kubeconfig=$KUBECONFIG" 0 "Retrieve results archive"
        rlAssertExists "$RESULTS_TAR"

        # 4. Parse results (report mode)
        rlRun "set -o pipefail; $SUDO_PREFIX $SONOBUOY_CMD results $RESULTS_TAR --mode=report 2>&1 | tee $RESULTS_LOG" 0 "Parse sonobuoy results (report mode)"

        # 5. Assert summary counts
        rlAssertGrep "Passed: $EXPECT_PASSED" "$RESULTS_LOG"
        rlAssertGrep "Failed: $EXPECT_FAILED" "$RESULTS_LOG"
        rlAssertGrep "Total: $EXPECT_TOTAL" "$RESULTS_LOG"

        # 6. Assert every node passed
        rlAssertGrep "Status: passed" "$RESULTS_LOG"
        rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        # Remove cluster resources (distinct from binary removal in k8sLibCleanup)
        rlRun "$SUDO_PREFIX $SONOBUOY_CMD delete --wait --kubeconfig=$KUBECONFIG || true" 0 "Delete sonobuoy cluster resources"
        rlRun "rm -f $RESULTS_TAR $RESULTS_LOG" 0 "Remove results archive and log"
        rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
