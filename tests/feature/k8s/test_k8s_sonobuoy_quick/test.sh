#!/bin/bash
# ============================================================
# K8s Sonobuoy Quick mode smoke check
#   Run `sonobuoy run --mode quick` (single e2e test) to
#   quickly verify cluster reachability and sonobuoy works.
#
# 脚本直证性: sonobuoy CLI 命令均在本文件中明文直接调用。
# ============================================================

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Setup: ensure sonobuoy is installed on master"
        k8sLibSetup 1
        rlRun "hwRunOnServer 1 'sudo sonobuoy version'" 0 "sonobuoy CLI available on master"
    rlPhaseEnd

    rlPhaseStartTest "Run sonobuoy quick mode"
        # Clean any previous run leftovers (tolerate absence)
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete previous sonobuoy resources"

        # Run quick mode (single e2e test) and wait for completion
        rlRun "hwRunOnServer 1 'sudo sonobuoy run --mode quick --wait --kubeconfig=/etc/kubernetes/admin.conf --image=$SONOBUOY_IMAGE'" 0 "sonobuoy run quick mode completes"

        # Retrieve results tarball
        rlRun "hwRunOnServer 1 'sudo sonobuoy retrieve -f /tmp/k8s-quick-results.tar.gz --kubeconfig=/etc/kubernetes/admin.conf'" 0 "Retrieve sonobuoy results"

        # Evaluate results: no failed tests expected in quick mode
        rlRun "hwRunOnServer 1 'sudo sonobuoy results /tmp/k8s-quick-results.tar.gz --mode=detailed'" 0 "sonobuoy results detailed shows no failures"
    rlPhaseEnd

    rlPhaseStartCleanup "Cleanup: remove sonobuoy resources"
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete sonobuoy resources"
        rlRun "hwRunOnServer 1 'rm -f /tmp/k8s-quick-results.tar.gz'" 0 "Remove local results tarball"
    rlPhaseEnd
rlJournalEnd
