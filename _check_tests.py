import os, re

def check_test(base_dir):
    for d in sorted(os.listdir(base_dir)):
        dpath = os.path.join(base_dir, d)
        if not os.path.isdir(dpath):
            continue
        tf = os.path.join(dpath, 'test.sh')
        if not os.path.exists(tf):
            continue
        with open(tf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f'--- {d} ---')
        rl_run_lines = re.findall(r'rlRun\s+"(.+?)"\s+\d+\s+"(.+?)"', content)
        for cmd, desc in rl_run_lines:
            print(f'  rlRun: {desc} | cmd: {cmd[:120]}')
        print()

check_test(r'E:\code\openruyi-autotest\tests\functional\pkgs\grep')