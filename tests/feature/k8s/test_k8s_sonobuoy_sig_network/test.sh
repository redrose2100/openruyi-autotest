#!/bin/bash
# ============================================================
# K8s e2e custom focus: sig-network (Sonobuoy)
#   Run `sonobuoy run --e2e-focus="\[sig-network\]"` to verify
#   the whole networking SIG test surface on RISC-V K8s.
#   Threshold: 100% pass on focused tests (design §6.3).
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

    rlPhaseStartTest "Run sonobuoy e2e focus sig-network"
        # Clean any previous run leftovers (tolerate absence)
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete previous sonobuoy resources"

        # Run with a custom e2e focus regex and wait.
        # NOTE: focus is single-quoted INSIDE cmd. rlRun evals its command
        # string, so a literal " in $cmd would be re-parsed and split the
        # argument. Single quotes inside $cmd survive eval as literal chars
        # and are re-parsed only on the remote side, keeping the regex intact.
        focus='\[sig-network\]'
        cmd="sudo sonobuoy run --e2e-focus='$focus' --wait --kubeconfig=/etc/kubernetes/admin.conf --image=$SONOBUOY_IMAGE"
        rlRun "hwRunOnServer 1 \"$cmd\"" 0 "sonobuoy run completes for sig-network"

        # Retrieve results tarball
        rlRun "hwRunOnServer 1 'sudo sonobuoy retrieve -f /tmp/k8s-sig-network-results.tar.gz --kubeconfig=/etc/kubernetes/admin.conf'" 0 "Retrieve sonobuoy results"

        # Evaluate results
        rlRun "hwRunOnServer 1 'sudo sonobuoy results /tmp/k8s-sig-network-results.tar.gz --mode=detailed'" 0 "sonobuoy results detailed runs"

        # Parse pass/fail counts and assert 100% pass rate
        summary=$(hwRunOnServer 1 "sudo sonobuoy results /tmp/k8s-sig-network-results.tar.gz" 2>/dev/null)
        rlLogInfo "Sonobuoy summary:"
        rlLogInfo "$summary"
        passed=$(echo "$summary" | awk -F': ' '/Passed:/{print $2}' | tr -d ' ')
        failed=$(echo "$summary" | awk -F': ' '/Failed:/{print $2}' | tr -d ' ')
        total=$(echo "$summary" | awk -F': ' '/Total:/{print $2}' | tr -d ' ')
        if [ -z "$total" ]; then
            rlFail "Cannot parse sonobuoy results summary"
        else
            rlLogInfo "Passed: $passed / $total"
            if [ "${failed:-0}" -eq 0 ] && [ "$total" -ge 1 ]; then
                rlPass "sig-network focused tests all passed ($passed/$total)"
            else
                rlFail "sig-network has $failed failed test(s) out of $total"
            fi
        fi
    rlPhaseEnd

    rlPhaseStartCleanup "Cleanup: remove sonobuoy resources"
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete sonobuoy resources"
        rlRun "hwRunOnServer 1 'rm -f /tmp/k8s-sig-network-results.tar.gz'" 0 "Remove local results tarball"
    rlPhaseEnd
rlJournalEnd
