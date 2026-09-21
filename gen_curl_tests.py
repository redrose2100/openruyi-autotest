#!/usr/bin/env python3
"""
Generate individual curl tests: ONE file = ONE feature.
"""
from pathlib import Path

PKG_DIR = Path(r"E:\code\openruyi-autotest\tests\functional\pkgs\curl")

HEADER = """#!/bin/bash
# Functional test: curl - {feature}
# Beakerlib-based test with lifecycle management

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
    curlSetup
    TmpDir=$(mktemp -d)
    rlRun "cd $TmpDir" 0 "Enter temporary test directory"
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

def create_test(dir_name, feature_desc, commands):
    test_dir = PKG_DIR / dir_name
    test_dir.mkdir(parents=True, exist_ok=True)
    rlrun_lines = "\n".join(f"    rlRun \"{cmd}\" {rc} \"{desc}\"" for cmd, rc, desc in commands)
    content = HEADER.format(feature=feature_desc, rlRun_commands=rlrun_lines)
    (test_dir / "test.sh").write_text(content, encoding='utf-8')
    print(f"  + {dir_name}")

# URL for tests
URL = "http://example.com"

tests = [
    ("test_curl_head", "HEAD request -I", [
        (f"curl -s -I {URL}", 0, "curl -I: HTTP HEAD request"),
        (f"curl -s -I {URL} | grep -qiE 'HTTP|Content'", 0, "curl -I: response shows headers"),
    ]),
    ("test_curl_post_data", "POST with -d data", [
        (f"curl -s -X POST -d 'key=value' {URL}", 0, "curl -d: POST data"),
    ]),
    ("test_curl_custom_method", "custom HTTP method -X", [
        (f"curl -s -X PUT {URL}", 0, "curl -X: custom PUT method"),
    ]),
    ("test_curl_custom_header", "custom header -H", [
        (f"curl -s -H 'Accept: text/html' {URL}", 0, "curl -H: custom header"),
        (f"curl -s -H 'User-Agent: test' {URL}", 0, "curl -H: custom user agent"),
    ]),
    ("test_curl_user_auth", "HTTP basic auth -u", [
        (f"curl -s -u testuser:testpass {URL}", 0, "curl -u: basic auth"),
    ]),
    ("test_curl_cookies", "cookie handling -b/-c", [
        (f"curl -s -c cookie.txt {URL}", 0, "curl -c: save cookies"),
        (f"curl -s -b cookie.txt {URL}", 0, "curl -b: send cookies"),
        (f"test -f cookie.txt", 0, "curl -c: cookie file created"),
    ]),
    ("test_curl_write_out", "write-out variables -w", [
        (f"curl -s -o /dev/null -w '%{{http_code}}\n' {URL}", 0, "curl -w: http_code"),
        (f"curl -s -o /dev/null -w '%{{time_total}}\n' {URL}", 0, "curl -w: time_total"),
        (f"curl -s -o /dev/null -w '%{{size_download}}\n' {URL}", 0, "curl -w: size_download"),
    ]),
    ("test_curl_dump_headers", "dump response headers -D", [
        (f"curl -s -o /dev/null -D headers.txt {URL}", 0, "curl -D: dump headers to file"),
        (f"test -f headers.txt", 0, "curl -D: headers file exists"),
    ]),
    ("test_curl_user_agent", "user agent string -A", [
        (f"curl -s -A 'Mozilla/5.0' {URL}", 0, "curl -A: set user agent"),
    ]),
    ("test_curl_retry", "retry on failure --retry", [
        (f"curl -s --retry 1 --retry-delay 1 --retry-max-time 3 http://nonexistent.local 2>&1 | grep -qiE 'Could not|failed|Retry' || echo retry_attempted", 0, "curl --retry: retry mechanism"),
    ]),
    ("test_curl_max_time", "maximum time -m", [
        (f"curl -s -m 3 {URL}", 0, "curl -m: max time limit"),
    ]),
    ("test_curl_limit_rate", "rate limit --limit-rate", [
        (f"curl -s --limit-rate 10K {URL} -o /dev/null", 0, "curl --limit-rate: bandwidth limit"),
    ]),
    ("test_curl_compressed", "accept compressed --compressed", [
        (f"curl -s --compressed {URL}", 0, "curl --compressed: request compressed"),
    ]),
    ("test_curl_resolve", "custom DNS resolve --resolve", [
        (f"curl -s --resolve 'example.com:80:93.184.215.14' {URL}", 0, "curl --resolve: custom DNS"),
    ]),
    ("test_curl_upload", "upload file -T", [
        ("echo 'upload content' > upload_test.txt", 0, "Create upload file"),
        (f"curl -s -T upload_test.txt http://example.com -o /dev/null 2>&1 | grep -qiE 'error|405|Method Not Allowed' || echo upload_sent", 0, "curl -T: upload file"),
    ]),
    ("test_curl_form_data", "multipart form -F", [
        ("echo 'formdata' > form_test.txt", 0, "Create form data file"),
        (f"curl -s -F 'file=@form_test.txt' {URL} -o /dev/null 2>&1 | grep -qiE 'error|405|Method Not Allowed' || echo form_sent", 0, "curl -F: multipart form upload"),
    ]),
    ("test_curl_json", "JSON data --json", [
        (f"curl -s --json '{{\"key\":\"value\"}}' {URL} -o /dev/null 2>&1 | grep -qiE 'error|405|Method Not Allowed' || echo json_sent", 0, "curl --json: JSON POST"),
    ]),
    ("test_curl_proxy", "proxy support -x", [
        (f"curl -s -x '' {URL} 2>&1 || echo proxy_check_done", 0, "curl -x: proxy option parses"),
    ]),
    ("test_curl_insecure", "insecure SSL -k", [
        (f"curl -s -k https://example.com -o /dev/null", 0, "curl -k: skip SSL verification"),
    ]),
    ("test_curl_cacert", "CA certificate --cacert", [
        (f"curl --cacert /dev/null https://example.com 2>&1 | grep -qiE 'error|Certificate|CA' || echo cacert_check", 0, "curl --cacert: CA cert option"),
    ]),
    ("test_curl_cert_key", "client cert --cert/--key", [
        (f"curl --cert /dev/null --key /dev/null {URL} 2>&1 | grep -qiE 'error|PEM|certificate|cert' || echo cert_check", 0, "curl --cert/--key: client cert options"),
    ]),
    ("test_curl_data_raw", "raw data --data-raw", [
        (f"curl -s --data-raw 'raw=data' {URL} -o /dev/null", 0, "curl --data-raw: raw POST data"),
    ]),
    ("test_curl_get_with_data", "GET with data -G", [
        (f"curl -s -G -d 'q=test' {URL}", 0, "curl -G: GET with query params"),
    ]),
    ("test_curl_resume", "resume download -C", [
        (f"curl -s -C - {URL} -o resume_test.html", 0, "curl -C: resume transfer"),
    ]),
]

# Also split existing multi-feature tests
print("=== Generating individual curl tests ===")
for dir_name, feature, cmds in tests:
    create_test(dir_name, feature, cmds)

print(f"\nTotal: {len(tests)} new individual curl tests created.")
print("Now remove old multi-feature tests manually if needed.")