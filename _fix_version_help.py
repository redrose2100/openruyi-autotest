import os, re

base = r'tests\functional\pkgs'

# Fix pattern: rlRun "cmd 2>&1 | grep -qiE "...error..." version/help check
# → rlRun "cmd 2>&1" 0 "version/help check"
# This fixes cases where the command works fine but grep finds no error text

total = 0
to_fix = []

for root, dirs, files in os.walk(base):
    for f in files:
        if f == 'test.sh':
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            # Find lines with grep -qiE "error|..." but the command is version/help
            lines = content.split('\n')
            new_lines = []
            modified = False
            
            for line in lines:
                if 'grep -qiE' in line and 'error|Error|not found|No such|Unable to' in line:
                    # Check if command is --version or --help
                    if '--version' in line or '--help' in line:
                        # Extract the command before the pipe
                        # Pattern: rlRun "cmd 2>&1 | grep -qiE "..." " 0 "desc"
                        m = re.match(r'(\s*rlRun\s+")(.+?)\s*2>&1\s*\|\s*grep\s+-qiE\s+\"error\|Error\|not found\|No such\|Unable to\"(\s*"\s*)(\d+)(\s*")(.+)', line)
                        if m:
                            prefix = m.group(1)
                            cmd = m.group(2)
                            mid = m.group(3)
                            old_exit = m.group(4)
                            suffix = m.group(5)
                            desc = m.group(6)
                            # Simplify: just run the command
                            new_line = f'{prefix}{cmd} 2>&1{mid}0{suffix}{desc}'
                            new_lines.append(new_line)
                            modified = True
                            continue
                
                new_lines.append(line)
            
            if modified:
                new_content = '\n'.join(new_lines)
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
                rel = os.path.relpath(fp, base)
                print(f'Fixed version/help: {rel}')
                total += 1

print(f'\nTotal: {total} files fixed')