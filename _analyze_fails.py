import os, re

failing = {
    'bash': ('bash', 'test_bash_basic_script'),
    'authselect': ('authselect', 'test_authselect_basic'),
    'git': ('git', 'test_git_tag_operations'),
    'iputils_ping': ('iputils', 'test_iputils_ping_basic_functionality'),
    'iputils_trace': ('iputils', 'test_iputils_tracepath'),
    'cmake_basic': ('cmake', 'test_cmake_basic_cmake_project'),
    'cmake_ver': ('cmake', 'test_cmake_cmake_version_and_help'),
    'jitterentropy': ('jitterentropy', 'test_jitterentropy_files'),
    'labwc': ('labwc', 'test_labwc_configuration'),
    'binutils': ('binutils', 'test_binutils_objcopy'),
    'ca_cert': ('ca-certificates', 'test_ca_certificates_version_help'),
    'coreutils': ('coreutils', 'test_coreutils_error_handling'),
    'elfutils': ('elfutils', 'test_elfutils_version_help'),
    'cloud_grow': ('cloud-utils-growpart', 'test_cloud_utils_growpart_dry_run__no_actual_resize'),
}

lib_pkgs = ['libaio', 'libarchive', 'libbpf', 'libcap-ng', 'libcap', 'libeconf', 'libedit', 'libevent', 'libffi', 'libgcrypt', 'libmnl', 'libnetfilter_conntrack', 'libnfnetlink', 'libnftnl', 'libpng']

base = r'E:\code\openruyi-autotest\tests\functional\pkgs'

for key, (pkg, test) in failing.items():
    fp = os.path.join(base, pkg, test, 'test.sh')
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            c = f.read()
        runs = re.findall(r'rlRun\s+"(.+?)"\s+(\S+)\s+"(.+?)"', c)
        print(f'=== {pkg}/{test} ({len(runs)} rlRun) ===')
        for cmd, exit_val, desc in runs:
            print(f'  exit={exit_val}: {desc}')
        print()

for pkg in lib_pkgs:
    fp = os.path.join(base, pkg, f'test_{pkg}_files', 'test.sh')
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            c = f.read()
        runs = re.findall(r'rlRun\s+"(.+?)"\s+(\S+)\s+"(.+?)"', c)
        print(f'=== {pkg}/test_{pkg}_files ({len(runs)} rlRun) ===')
        for cmd, exit_val, desc in runs:
            print(f'  exit={exit_val}: {desc}')
        print()