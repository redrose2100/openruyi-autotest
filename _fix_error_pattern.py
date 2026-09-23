import os, re, glob

base = r'E:\code\openruyi-autotest\tests\functional\pkgs'

# Pattern 1: Fix error handling with || echo expected-error
# "cmd | grep -qiE ... || echo expected-error" 1 → "cmd | grep -qiE ..." 0
pattern1 = re.compile(
    r'(rlRun\s+")(.+?)(\s*\|\s*grep\s+-qiE\s+"error\|Error\|not found\|No such\|Unable to"[^|]*)'
    r'(\s*\|\|\s*echo\s+expected-error\s*)("\s+1\s+")(.+)',
    re.DOTALL
)

# Pattern 2: Fix error handling with | grep ... || echo expected-error
# When the last grep expects to FIND errors (exit 0)
def fix_error_handling(content):
    # Match: rlRun "cmd 2>&1 | grep -qiE "error|..." || echo expected-error" 1 "desc"
    # Fix:  rlRun "cmd 2>&1 | grep -qiE "error|..."" 0 "desc"
    
    lines = content.split('\n')
    new_lines = []
    modified = False
    
    for line in lines:
        new_line = line
        
        # Pattern: | grep -qiE "...error..." || echo expected-error" N (where N is 1 or another number)
        m = re.search(
            r'(rlRun\s+".+?)\|\s*grep\s+-qiE\s+"(error\|Error\|not found\|No such\|Unable to)"\s*'
            r'\|\|\s*echo\s+expected-error(\s*"\s*)(\d+)(\s*".*)',
            line
        )
        if m:
            # Remove || echo expected-error, change the exit code
            new_line = re.sub(
                r'\|\|\s*echo\s+expected-error\s*"\s*\d+\s*"',
                '" 0 "',
                line
            )
            modified = True
        
        new_lines.append(new_line)
    
    return '\n'.join(new_lines), modified

# Track changes
total_fixed = 0
total_files = 0

# Walk all pkgs tests
for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'test.sh':
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            new_content, modified = fix_error_handling(content)
            
            if modified:
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
                rel = os.path.relpath(fp, base)
                print(f'Fixed: {rel}')
                total_fixed += 1
            
            total_files += 1

print(f'\nTotal: {total_fixed} files fixed out of {total_files}')