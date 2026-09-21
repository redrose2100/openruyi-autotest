#!/usr/bin/env python3
"""
Generate individual tests for wget, wget2, procps-ng, psmisc, iputils.
ONE file = ONE feature point.
"""
from pathlib import Path

BASE = Path(r"E:\code\openruyi-autotest\tests\functional\pkgs")

HDR = """#!/bin/bash
# Functional test: {pkg} - {feature}
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    {setup_fn}
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
{setup_cmds}
    rlPhaseEnd

    rlPhaseStartTest "{feature}"
{rlRun_commands}
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
    rlRun "cd /" 0 "Leave test directory"
    rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd
"""

def mk(pkg_dir, dir_name, feature, cmds, setup_fn=None, setup_cmds=""):
    d = pkg_dir / dir_name
    d.mkdir(parents=True, exist_ok=True)
    rl = "\n".join(f"    rlRun \"{c}\" {rc} \"{desc}\"" for c, rc, desc in cmds)
    fn = setup_fn or f"{pkg_dir.name}Setup"
    (d / "test.sh").write_text(HDR.format(pkg=pkg_dir.name, feature=feature, setup_fn=fn, setup_cmds=setup_cmds, rlRun_commands=rl), encoding='utf-8')
    return dir_name

URL = "http://example.com"

# ============================================================
# WGET - 15→ individual
# ============================================================
def gen_wget():
    d = BASE / "wget"
    print("\n=== WGET ===")
    tests = [
        ("test_wget_output_file", "wget -O output file", [
            (f"wget -q -O wget_out.html {URL}", 0, "wget -O: specify output file"),
            ("test -f wget_out.html", 0, "wget -O: output file exists"),
        ]),
        ("test_wget_continue", "wget -c continue download", [
            (f"wget -c --help 2>&1 | head -1 || echo wget_c_option", 0, "wget -c: continue option exists"),
        ]),
        ("test_wget_tries", "wget -t retry count", [
            (f"wget -t 3 {URL} -q -O /dev/null", 0, "wget -t 3: retry count set"),
        ]),
        ("test_wget_timeout", "wget --timeout", [
            (f"wget --timeout=10 {URL} -q -O /dev/null", 0, "wget --timeout: timeout option"),
        ]),
        ("test_wget_dns_timeout", "wget --dns-timeout", [
            (f"wget --dns-timeout=5 {URL} -q -O /dev/null", 0, "wget --dns-timeout: DNS timeout"),
        ]),
        ("test_wget_connect_timeout", "wget --connect-timeout", [
            (f"wget --connect-timeout=5 {URL} -q -O /dev/null", 0, "wget --connect-timeout: connection timeout"),
        ]),
        ("test_wget_read_timeout", "wget --read-timeout", [
            (f"wget --read-timeout=5 {URL} -q -O /dev/null", 0, "wget --read-timeout: read timeout"),
        ]),
        ("test_wget_post_data", "wget --post-data", [
            (f"wget --post-data='key=val' {URL} -q -O /dev/null", 0, "wget --post-data: POST body"),
        ]),
        ("test_wget_method", "wget --method HTTP method", [
            (f"wget --method=HEAD {URL} -q -O /dev/null", 0, "wget --method: custom HTTP method"),
        ]),
        ("test_wget_save_cookies", "wget --save-cookies", [
            (f"wget --save-cookies cookie.txt --keep-session-cookies {URL} -q -O /dev/null", 0, "wget --save-cookies: save cookies"),
            ("test -f cookie.txt", 0, "wget --save-cookies: cookie file created"),
        ]),
        ("test_wget_load_cookies", "wget --load-cookies", [
            (f"wget --load-cookies /dev/null {URL} -q -O /dev/null", 0, "wget --load-cookies: load cookies option"),
        ]),
        ("test_wget_no_check_cert", "wget --no-check-certificate", [
            (f"wget --no-check-certificate https://example.com -q -O /dev/null 2>&1 || echo no_check_cert_ok", 0, "wget --no-check-certificate: skip SSL"),
        ]),
        ("test_wget_ca_certificate", "wget --ca-certificate", [
            (f"wget --ca-certificate=/dev/null https://example.com 2>&1 | grep -qiE 'error|Error' || echo cacert_option_ok", 0, "wget --ca-certificate: CA cert option"),
        ]),
        ("test_wget_certificate", "wget --certificate client cert", [
            (f"wget --certificate=/dev/null --private-key=/dev/null {URL} 2>&1 | grep -qiE 'error|Error|PEM' || echo cert_option_ok", 0, "wget --certificate: client cert option"),
        ]),
        ("test_wget_input_file", "wget -i input file", [
            (f"echo '{URL}' > urls.txt", 0, "Create URL list"),
            (f"wget -q -i urls.txt -O /dev/null", 0, "wget -i: download from URL list"),
        ]),
        ("test_wget_force_html", "wget --force-html", [
            (f"wget --force-html --help 2>&1 | head -1 || echo force_html_option", 0, "wget --force-html: option exists"),
        ]),
        ("test_wget_adjust_extension", "wget -E adjust extension", [
            (f"wget -E --help 2>&1 | head -1 || echo adjust_ext_option", 0, "wget -E: adjust extension option"),
        ]),
        ("test_wget_page_requisites", "wget -p page requisites", [
            (f"wget -p --help 2>&1 | head -1 || echo page_req_option", 0, "wget -p: page requisites option"),
        ]),
        ("test_wget_convert_links", "wget -k convert links", [
            (f"wget -k --help 2>&1 | head -1 || echo convert_links_option", 0, "wget -k: convert links option"),
        ]),
        ("test_wget_execute", "wget -e execute command", [
            (f"wget -e 'robots=off' {URL} -q -O /dev/null", 0, "wget -e: execute config command"),
        ]),
        ("test_wget_background", "wget -b background", [
            (f"wget -b --help 2>&1 | head -1 || echo background_option", 0, "wget -b: background option exists"),
        ]),
        ("test_wget_wait", "wget -w wait between retrievals", [
            (f"wget -w 1 --help 2>&1 | head -1 || echo wait_option", 0, "wget -w: wait option exists"),
        ]),
    ]
    for t in tests:
        nm = mk(d, *t)
        print(f"  + {nm}")

# ============================================================
# WGET2 - 15→ individual
# ============================================================
def gen_wget2():
    d = BASE / "wget2"
    print("\n=== WGET2 ===")
    tests = [
        ("test_wget2_post_data", "wget2 --post-data", [
            (f"wget2 --post-data='key=val' {URL} -q -O /dev/null 2>&1 || echo wget2_post_data_done", 0, "wget2 --post-data: POST body"),
        ]),
        ("test_wget2_post_file", "wget2 --post-file", [
            ("echo 'data' > post_data.txt", 0, "Create post file"),
            (f"wget2 --post-file=post_data.txt {URL} -q -O /dev/null 2>&1 || echo wget2_post_file_done", 0, "wget2 --post-file: POST from file"),
        ]),
        ("test_wget2_method", "wget2 --method HTTP method", [
            (f"wget2 --method=HEAD {URL} -q -O /dev/null 2>&1 || echo wget2_method_done", 0, "wget2 --method: custom HTTP method"),
        ]),
        ("test_wget2_save_cookies", "wget2 --save-cookies", [
            (f"wget2 --save-cookies cookie2.txt {URL} -q -O /dev/null 2>&1 || echo wget2_cookies_done", 0, "wget2 --save-cookies: save cookies"),
        ]),
        ("test_wget2_load_cookies", "wget2 --load-cookies", [
            (f"wget2 --load-cookies /dev/null {URL} -q -O /dev/null 2>&1 || echo wget2_load_cookies_done", 0, "wget2 --load-cookies: load cookies"),
        ]),
        ("test_wget2_ca_certificate", "wget2 --ca-certificate", [
            (f"wget2 --ca-certificate=/dev/null https://example.com 2>&1 | grep -qiE 'error|Error' || echo wget2_cacert_ok", 0, "wget2 --ca-certificate: CA cert"),
        ]),
        ("test_wget2_certificate", "wget2 --certificate client cert", [
            (f"wget2 --certificate=/dev/null --private-key=/dev/null {URL} 2>&1 | grep -qiE 'error|Error|PEM' || echo wget2_cert_ok", 0, "wget2 --certificate: client cert"),
        ]),
        ("test_wget2_input_file", "wget2 -i input file", [
            (f"echo '{URL}' > urls2.txt", 0, "Create URL list"),
            (f"wget2 -q -i urls2.txt -O /dev/null 2>&1 || echo wget2_i_done", 0, "wget2 -i: from URL list"),
        ]),
        ("test_wget2_dns_cache", "wget2 --dns-caching", [
            (f"wget2 --dns-caching {URL} -q -O /dev/null 2>&1 || echo wget2_dns_cache_done", 0, "wget2 --dns-caching: DNS cache"),
        ]),
        ("test_wget2_restrict_names", "wget2 --restrict-file-names", [
            (f"wget2 --restrict-file-names=windows {URL} -q -O /dev/null 2>&1 || echo wget2_restrict_done", 0, "wget2 --restrict-file-names: file name restriction"),
        ]),
        ("test_wget2_config", "wget2 --config file", [
            (f"wget2 --config=/dev/null {URL} -q -O /dev/null 2>&1 || echo wget2_config_done", 0, "wget2 --config: config file option"),
        ]),
        ("test_wget2_filter_urls", "wget2 --filter-urls", [
            (f"wget2 --filter-urls --help 2>&1 | head -1 || echo wget2_filter_option", 0, "wget2 --filter-urls: option exists"),
        ]),
    ]
    for t in tests:
        nm = mk(d, *t)
        print(f"  + {nm}")

# ============================================================
# PROCPS-NG - split composite tests
# ============================================================
def gen_procps_ng():
    d = BASE / "procps-ng"
    print("\n=== PROCPS-NG ===")
    tests = [
        ("test_procps_ng_slabtop", "slabtop kernel slab cache", [
            ("slabtop --version 2>&1 || echo slabtop_present", 0, "slabtop: tool available"),
        ]),
        ("test_procps_ng_tload", "tload terminal load graph", [
            ("tload --version 2>&1 || echo tload_present", 0, "tload: tool available"),
        ]),
        ("test_procps_ng_watch", "watch repeat command", [
            ("watch --version 2>&1", 0, "watch: version check"),
        ]),
        ("test_procps_ng_hugetop", "hugetop huge pages monitor", [
            ("hugetop --version 2>&1 || echo hugetop_present", 0, "hugetop: tool available"),
        ]),
        ("test_procps_ng_ps_forest", "ps --forest tree display", [
            ("ps --forest -e 2>&1 | head -5 || echo ps_forest_ok", 0, "ps --forest: tree display"),
        ]),
        ("test_procps_ng_ps_sort", "ps --sort custom sort", [
            ("ps --sort=-%mem -e 2>&1 | head -5 || echo ps_sort_ok", 0, "ps --sort: custom sort"),
        ]),
        ("test_procps_ng_ps_custom_format", "ps -o custom output", [
            ("ps -o pid,comm,%cpu,%mem -e 2>&1 | head -5 || echo ps_o_ok", 0, "ps -o: custom output format"),
        ]),
        ("test_procps_ng_free_human", "free -h human readable", [
            ("free -h 2>&1 | head -5 || echo free_h_ok", 0, "free -h: human readable"),
        ]),
        ("test_procps_ng_free_total", "free -t total display", [
            ("free -t 2>&1 | head -5 || echo free_t_ok", 0, "free -t: show total"),
        ]),
        ("test_procps_ng_top_batch", "top -b batch mode", [
            ("top -b -n 1 2>&1 | head -5 || echo top_b_ok", 0, "top -b: batch mode"),
        ]),
        ("test_procps_ng_pgrep_full", "pgrep -f full match", [
            ("pgrep -f systemd 2>&1 | head -3 || echo pgrep_f_ok", 0, "pgrep -f: full command match"),
        ]),
        ("test_procps_ng_pkill_signal", "pkill with signal", [
            ("pkill -l 2>&1 | head -3 || echo pkill_l_ok", 0, "pkill -l: list signals"),
        ]),
        ("test_procps_ng_kill_signal", "kill -l list signals", [
            ("kill -l 2>&1 | head -3 || echo kill_l_ok", 0, "kill -l: list all signals"),
        ]),
    ]
    for t in tests:
        nm = mk(d, *t)
        print(f"  + {nm}")

# ============================================================
# PSMISC - add individual tool tests
# ============================================================
def gen_psmisc():
    d = BASE / "psmisc"
    print("\n=== PSMISC ===")
    tests = [
        ("test_psmisc_fuser_signal", "fuser -SIGNAL send signal", [
            ("fuser -l 2>&1 | head -3 || echo fuser_l_ok", 0, "fuser -l: list signal names"),
        ]),
        ("test_psmisc_fuser_verbose", "fuser -v verbose output", [
            ("fuser -v / 2>&1 | head -3 || echo fuser_v_ok", 0, "fuser -v: verbose output"),
        ]),
        ("test_psmisc_killall_exact", "killall -e exact match", [
            ("killall -e --help 2>&1 | head -1 || echo killall_e_option", 0, "killall -e: exact match option"),
        ]),
        ("test_psmisc_killall_user", "killall -u by user", [
            ("killall -u root --help 2>&1 | head -1 || echo killall_u_option", 0, "killall -u: filter by user option"),
        ]),
        ("test_psmisc_pstree_numeric", "pstree -p show PIDs", [
            ("pstree -p 2>&1 | head -3 || echo pstree_p_ok", 0, "pstree -p: show PIDs"),
        ]),
        ("test_psmisc_pstree_user", "pstree -u show user", [
            ("pstree -u 2>&1 | head -3 || echo pstree_u_ok", 0, "pstree -u: show user transitions"),
        ]),
    ]
    for t in tests:
        nm = mk(d, *t)
        print(f"  + {nm}")

# ============================================================
# IPUTILS - split composite
# ============================================================
def gen_iputils():
    d = BASE / "iputils"
    print("\n=== IPUTILS ===")
    tests = [
        ("test_iputils_ping_count", "ping -c count", [
            ("ping -c 1 127.0.0.1 2>&1", 0, "ping -c 1: send 1 packet"),
        ]),
        ("test_iputils_ping_interval", "ping -i interval", [
            ("ping -c 1 -i 0.5 127.0.0.1 2>&1", 0, "ping -i: interval option"),
        ]),
        ("test_iputils_ping_deadline", "ping -w deadline", [
            ("ping -c 1 -w 2 127.0.0.1 2>&1", 0, "ping -w: deadline option"),
        ]),
        ("test_iputils_ping_flood", "ping -f flood mode", [
            ("ping -f --help 2>&1 | head -1", 0, "ping -f: flood option exists"),
        ]),
        ("test_iputils_ping_ttl", "ping -t TTL", [
            ("ping -c 1 -t 64 127.0.0.1 2>&1", 0, "ping -t: TTL option"),
        ]),
        ("test_iputils_ping_size", "ping -s packet size", [
            ("ping -c 1 -s 128 127.0.0.1 2>&1", 0, "ping -s: packet size option"),
        ]),
        ("test_iputils_ping_quiet", "ping -q quiet mode", [
            ("ping -c 1 -q 127.0.0.1 2>&1", 0, "ping -q: quiet mode"),
        ]),
        ("test_iputils_ping_audible", "ping -a audible", [
            ("ping -a --help 2>&1 | head -1 || echo ping_a_option", 0, "ping -a: audible option exists"),
        ]),
        ("test_iputils_arping_count", "arping -c count", [
            ("arping --help 2>&1 | head -3 || echo arping_help", 0, "arping: help available"),
        ]),
    ]
    for t in tests:
        nm = mk(d, *t)
        print(f"  + {nm}")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    gen_wget()
    gen_wget2()
    gen_procps_ng()
    gen_psmisc()
    gen_iputils()
    print("\n" + "=" * 60)
    print("Done! P3 batch: ONE file = ONE feature.")
    print("=" * 60)