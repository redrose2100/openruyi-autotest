#!/bin/bash
# K8s feature test: cluster ready precheck
# Verify the RISC-V K8s cluster is ready before running sonobuoy smoke:
#   - kubectl CLI available
#   - kubeconfig readable (admin.conf)
#   - kubectl can reach the cluster API
#   - all nodes are Ready (expect 2: master + worker)
#
# Runs LOCALLY on the K8s master node (tmt provision: local).

. /usr/share/beakerlib/beakerlib.sh || exit 1

K8S_KUBECONFIG="/etc/kubernetes/admin.conf"
EXPECT_NODES=2

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        rlRun "id" 0 "Current user"
        rlRun "uname -m" 0 "Architecture (expect riscv64)"
        rlPhaseEnd

    rlPhaseStartTest "K8s cluster ready precheck"
        # 1. kubectl CLI available
        rlRun "command -v kubectl" 0 "kubectl CLI is available"

        # 2. kubeconfig exists and readable
        if [ ! -r "$K8S_KUBECONFIG" ]; then
            rlFail "kubeconfig not readable: $K8S_KUBECONFIG"
        else
            rlPass "kubeconfig readable: $K8S_KUBECONFIG"
        fi

        # 3. kubectl can reach the cluster API
        rlRun "kubectl --kubeconfig=$K8S_KUBECONFIG version --client" 0 "kubectl client version"
        rlRun "kubectl --kubeconfig=$K8S_KUBECONFIG cluster-info" 0 "Cluster API reachable"

        # 4. All nodes Ready (expect 2)
        local node_count ready_count
        node_count=$(kubectl --kubeconfig=$K8S_KUBECONFIG get nodes --no-headers 2>/dev/null | wc -l)
        ready_count=$(kubectl --kubeconfig=$K8S_KUBECONFIG get nodes --no-headers 2>/dev/null | awk '{print $2}' | grep -c '^Ready$')
        rlLogInfo "Node count: $node_count, Ready count: $ready_count (expect $EXPECT_NODES)"
        if [ "$node_count" -eq "$EXPECT_NODES" ] && [ "$ready_count" -eq "$EXPECT_NODES" ]; then
            rlPass "All $EXPECT_NODES nodes are Ready"
        else
            rlFail "Expected $EXPECT_NODES Ready nodes, got $node_count total / $ready_count Ready"
            kubectl --kubeconfig=$K8S_KUBECONFIG get nodes -o wide
        fi
        rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
