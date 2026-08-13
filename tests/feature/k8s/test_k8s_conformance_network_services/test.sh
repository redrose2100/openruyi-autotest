#!/bin/bash
# ============================================================
# K8s conformance - network services
#   Run `sonobuoy run --mode non-disruptive-conformance`
#   with an explicit --e2e-focus regex (16 tests).
#   Result judgement (design 6.3): every failed test item is
#   classified individually - items matching KNOWN_UNSUPPORTED
#   are reported as SKIP subresults, everything else FAILs the
#   case. No pass-rate threshold is used.
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

    rlPhaseStartTest "Run sonobuoy conformance (16 tests)"
        # Clean any previous run leftovers (tolerate absence)
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete previous sonobuoy resources"

        # Run non-disruptive conformance with the group focus regex and wait.
        # NOTE: focus is single-quoted INSIDE cmd. rlRun evals its command
        # string, so a literal " in $cmd would be re-parsed and split the
        # argument (or even cause a syntax error with regex parens). Single
        # quotes inside $cmd survive eval as literal chars and are re-parsed
        # only on the remote side, keeping the regex intact.
        focus='\[sig-network\].*(Services|Service endpoints latency)'
        cmd="sudo sonobuoy run --mode non-disruptive-conformance --e2e-focus='$focus' --wait --kubeconfig=/etc/kubernetes/admin.conf --image=$SONOBUOY_IMAGE"
        rlRun "hwRunOnServer 1 \"$cmd\"" 0 "sonobuoy run completes for focus group"

        # Retrieve results tarball
        rlRun "hwRunOnServer 1 'sudo sonobuoy retrieve -f /tmp/k8s-results.tar.gz --kubeconfig=/etc/kubernetes/admin.conf'" 0 "Retrieve sonobuoy results"

        # Evaluate results: fetch detailed per-test items (one JSON object
        # per line: {"name":"...","status":"...","meta":{...}}).
        detailed=$(hwRunOnServer 1 "sudo sonobuoy results /tmp/k8s-results.tar.gz --mode=detailed" 2>/dev/null)
        rlLogInfo "Sonobuoy detailed result items:"
        rlLogInfo "$detailed"

        # Per-item classification: a failed item matching a KNOWN_UNSUPPORTED
        # pattern is a RISC-V unsupported test -> SKIP subresult (does not fail
        # the case). Any other failed item is a real failure -> FAIL subresult.
        # KNOWN_UNSUPPORTED: grep -E alternation (e.g. 'pattern1|pattern2'),
        # overridable via the environment (populated from real runs, design 6.3).
        : "${KNOWN_UNSUPPORTED:-}"
        real_failures=0
        if [ -z "$detailed" ]; then
            rlFail "Cannot parse sonobuoy detailed results"
        else
            while IFS= read -r item; do
                # Only failed/timeout items need classification; skip passed/skipped.
                case "$item" in
                    *'"status":"failed"'*|*'"status":"timeout"'*) : ;;
                    *) continue ;;
                esac
                name=$(printf '%s' "$item" | sed -n 's/.*"name":"\([^"]*\)".*/\1/p')
                [ -n "$name" ] || continue
                safe_name=$(printf '%s' "$name" | tr "'" "_")
                if [ -n "$KNOWN_UNSUPPORTED" ] && printf '%s' "$name" | grep -Eq -- "$KNOWN_UNSUPPORTED"; then
                    rlLogInfo "Known unsupported on RISC-V, reporting SKIP: $name"
                    rlRun "tmt-report-result '/$safe_name' SKIP" 0 "Report $safe_name as skipped (unsupported on RISC-V)"
                else
                    rlRun "tmt-report-result '/$safe_name' FAIL" 0 "Report $safe_name as failed"
                    real_failures=$((real_failures + 1))
                fi
            done <<< "$detailed"
            rlLogInfo "Real failures in focus group: $real_failures"
            if [ "$real_failures" -eq 0 ]; then
                rlPass "Conformance focus group passed (16 tests, no unsupported-classified failures)"
            else
                rlFail "Conformance focus group has $real_failures real failure(s)"
            fi
        fi
    rlPhaseEnd

    rlPhaseStartCleanup "Cleanup: remove sonobuoy resources"
        rlRun "hwRunOnServer 1 'sudo sonobuoy delete --wait --kubeconfig=/etc/kubernetes/admin.conf || true'" 0 "Delete sonobuoy resources"
        rlRun "hwRunOnServer 1 'rm -f /tmp/k8s-results.tar.gz'" 0 "Remove local results tarball"
    rlPhaseEnd
rlJournalEnd
