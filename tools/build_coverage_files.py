#!/usr/bin/env python3
"""Generate per-package coverage files from functional-coverage.md and update READMEs."""
import re, os, shutil

BASE = r"e:\code\openruyi-autotest"
SRC = os.path.join(BASE, "docs", "coverage", "functional-coverage.md")
OUT_DIR = os.path.join(BASE, "docs", "coverage", "functional-coverage")
README = os.path.join(BASE, "README.md")
README_CN = os.path.join(BASE, "README_CN.md")

def get_all_packages():
    pkgs_dir = os.path.join(BASE, "tests", "functional", "pkgs")
    return sorted([d for d in os.listdir(pkgs_dir) if os.path.isdir(os.path.join(pkgs_dir, d))])

ALL_PACKAGES = set(get_all_packages())

def parse_functional_coverage(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r'## (\w[\w-]*)\n\n<details>\n<summary><b>\1 — \d+ 个用例 / \d+ 个功能点</b></summary>\n\n(.*?)\n\n</details>'
    package_details = {}
    for m in re.finditer(pattern, content, re.DOTALL):
        pkg = m.group(1)
        body = m.group(2)
        testsuites = []
        suite_pattern = r'#### (\S+)\n\n((?:- [^\n]+\n?)+)'
        for sm in re.finditer(suite_pattern, body):
            suite_name = sm.group(1)
            points_text = sm.group(2)
            test_points = [pline.strip()[2:] for pline in points_text.strip().split('\n') if pline.strip().startswith('- ')]
            testsuites.append({'suite': suite_name, 'points': test_points})
        package_details[pkg] = testsuites
    return package_details

def generate_package_md(pkg_name, testsuites):
    lines = [f"# {pkg_name} 功能测试覆盖详情", ""]
    total_suites = len(testsuites)
    total_points = sum(len(s['points']) for s in testsuites)
    lines.append(f"共 **{total_suites}** 个测试套，**{total_points}** 个测试点")
    lines.append("")
    lines.append("| Test Suite | Test Case | Test Point |")
    lines.append("|------------|-----------|------------|")
    for suite in testsuites:
        suite_name = suite['suite']
        points = suite['points']
        case_count = len(points)
        for i, point in enumerate(points):
            if i == 0:
                lines.append(f"| {suite_name} | {case_count} cases | {point} |")
            else:
                lines.append(f"| | | {point} |")
    return '\n'.join(lines) + '\n'

def update_readme_table(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern_12 = re.search(r'(###?\s*1\.2\s+[^\n]*)', content)
    if not pattern_12:
        print(f"  WARNING: Could not find 1.2 section in {readme_path}")
        return False

    section_start = pattern_12.start()
    table_start = content.find('| Category |', section_start)
    if table_start < 0:
        table_start = content.find('| 分类 |', section_start)
    if table_start < 0:
        print(f"  WARNING: Could not find table in 1.2 section of {readme_path}")
        return False

    next_pattern = re.search(r'\n(?:###?\s+1\.3|##\s+2\.\s|##\s+\S)', content[table_start:])
    if next_pattern:
        table_end = table_start + next_pattern.start()
    else:
        print(f"  WARNING: Could not find end of 1.2 table in {readme_path}")
        return False

    old_table = content[table_start:table_end]
    is_en = '| Category' in old_table.split('\n')[0]

    new_lines = []
    for line in old_table.strip('\n').split('\n'):
        line = line.rstrip()
        if not line.startswith('|'):
            continue
        if line.startswith('| Category') or line.startswith('| 分类'):
            hdr = "| Category | Representative Packages |" if is_en else "| 分类 | 代表性软件包 |"
            new_lines.append(hdr)
            new_lines.append("|----------|------------------------|")
            continue
        if line.startswith('|---') or line.startswith('|--'):
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            category = parts[1]
            pkgs_text = parts[2]
            new_pkgs = []
            for token in re.split(r',\s*', pkgs_text):
                token = token.strip()
                if not token:
                    continue
                base_name = re.sub(r'\s*\([^)]*\)', '', token).strip()
                if base_name in ALL_PACKAGES:
                    new_pkgs.append(f"[{token}](docs/coverage/functional-coverage/{base_name}.md)")
                else:
                    new_pkgs.append(token)
            new_pkgs_text = ', '.join(new_pkgs)
            new_lines.append(f"| {category} | {new_pkgs_text} |")

    new_table = '\n'.join(new_lines) + '\n'
    content = content.replace(old_table, new_table)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated {readme_path}")
    return True

if __name__ == '__main__':
    print("Step 1: Parsing functional-coverage.md...")
    details = parse_functional_coverage(SRC)
    print(f"  Parsed {len(details)} packages with test details")

    print("\nStep 2: Creating functional-coverage/ directory...")
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    for pkg_name, testsuites in details.items():
        md_content = generate_package_md(pkg_name, testsuites)
        filepath = os.path.join(OUT_DIR, f"{pkg_name}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
    print(f"  Generated {len(details)} package .md files")

    index_lines = ["# 功能测试覆盖详情 - 软件包索引", ""]
    index_lines.append(f"共 **{len(details)}** 个软件包")
    index_lines.append("")
    index_lines.append("| 软件包 | 测试套数 | 测试点数 |")
    index_lines.append("|--------|:---:|:---:|")
    for pkg_name, testsuites in details.items():
        suite_count = len(testsuites)
        point_count = sum(len(s['points']) for s in testsuites)
        index_lines.append(f"| [{pkg_name}]({pkg_name}.md) | {suite_count} | {point_count} |")
    with open(os.path.join(OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write('\n'.join(index_lines) + '\n')
    print("  Generated index.md")

    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("# Functional Test Coverage\n\n")
        f.write(f"This directory contains per-package test coverage details for **{len(details)}** RPM packages.\n\n")
        f.write("See [index.md](index.md) for a full package listing.\n")

    print("\nStep 3: Updating README.md section 1.2...")
    update_readme_table(README)

    print("\nStep 4: Updating README_CN.md section 1.2...")
    update_readme_table(README_CN)

    print(f"\nDone! Now delete: {SRC}")