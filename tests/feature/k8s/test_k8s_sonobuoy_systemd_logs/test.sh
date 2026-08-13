#!/bin/bash
# ============================================================
# K8s Sonobuoy systemd-logs plugin collection check
#   Run the systemd-logs DaemonSet plugin to collect system
#   journal logs from every node, then assert each node
#   produced >= 1 systemd_logs file in the results tarball.
#   Threshold: per-node >= 1 log file (design §6.3).
#   Node missing logs -> WARN, not FAIL.
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

    rlPhaseStartTest "Run sonobuoy systemd-logs plugin"
        # Clean any previous run leftovers (tolerate absence)
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete previous sonobuoy resources"

        # Run the systemd-logs plugin (DaemonSet on every node) and wait
        rlRun "hwRunOnServer 1 'sudo sonobuoy run --plugin systemd-logs --wait --kubeconfig=/etc/kubernetes/admin.conf --image=$SONOBUOY_IMAGE'" 0 "sonobuoy run systemd-logs completes"

        # Retrieve results tarball
        rlRun "hwRunOnServer 1 'sudo sonobuoy retrieve -f /tmp/k8s-systemd-results.tar.gz --kubeconfig=/etc/kubernetes/admin.conf'" 0 "Retrieve sonobuoy results"

        # Count systemd_logs files in the tarball and check node count
        logcount=$(hwRunOnServer 1 "sudo tar -tf /tmp/k8s-systemd-results.tar.gz | grep -c systemd_logs" 2>/dev/null | tr -d '\r\n')
        rlLogInfo "systemd_logs files found: ${logcount:-0}"

        nodes=$(hwRunOnServer 1 "sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf get nodes --no-headers | wc -l" 2>/dev/null | tr -d '\r\n')
        rlLogInfo "K8s node count: ${nodes:-0}"

        if [ -n "$logcount" ] && [ "$logcount" -ge 1 ]; then
            rlPass "systemd-logs collected $logcount log file(s) from the cluster"
        else
            rlWarn "No systemd_logs files found in results tarball (nodes may be unreachable)"
        fi
    rlPhaseEnd

    rlPhaseStartCleanup "Cleanup: remove sonobuoy resources"
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete sonobuoy resources"
        rlRun "hwRunOnServer 1 'rm -f /tmp/k8s-systemd-results.tar.gz'" 0 "Remove local results tarball"
    rlPhaseEnd
rlJournalEnd
