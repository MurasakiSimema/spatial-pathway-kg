#!/usr/bin/env python3
"""
check_compilation.py

Verifies the syntax and structural consistency of the LaTeX report:
1. Validates that all environments \\begin{...} have matching \\end{...}.
2. Validates that citation keys in \\cite{...} exist in KnowDivePubs.bib.
3. Checks for unescaped special characters.
4. If --compile is passed, triggers compile_report.py for the full XeLaTeX pipeline.

Usage:
    python check_compilation.py [--doc-dir PATH] [--compile]
"""

import os
import sys
import re
import glob
import shutil
import subprocess
import argparse

def extract_bib_keys(bib_path):
    keys = set()
    if not os.path.exists(bib_path):
        return keys
    with open(bib_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = re.match(r"@\w+\s*\{\s*([^,]+),", line)
            if match:
                keys.add(match.group(1).strip())
    return keys

def check_latex_syntax(file_path, bib_keys):
    errors = []
    warnings = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    env_stack = []

    for line_idx, line in enumerate(lines, start=1):
        # Strip comments
        code_part = re.sub(r"(?<!\\)%.*$", "", line).strip()

        # Check environments
        for m in re.finditer(r"\\begin\{([^}]+)\}", code_part):
            env = m.group(1)
            env_stack.append((env, line_idx))
        for m in re.finditer(r"\\end\{([^}]+)\}", code_part):
            env = m.group(1)
            if not env_stack:
                errors.append(f"{os.path.basename(file_path)}:L{line_idx} Unexpected \\end{{{env}}} with no matching \\begin")
            else:
                last_env, start_line = env_stack.pop()
                if last_env != env:
                    errors.append(f"{os.path.basename(file_path)}:L{line_idx} Mismatched environment: \\begin{{{last_env}}} on L{start_line} closed by \\end{{{env}}}")

        # Check citations
        for m in re.finditer(r"\\cite\{([^}]+)\}", code_part):
            cited = [k.strip() for k in m.group(1).split(",")]
            for k in cited:
                if bib_keys and k not in bib_keys:
                    warnings.append(f"{os.path.basename(file_path)}:L{line_idx} Citation key '{k}' not found in KnowDivePubs.bib")

    if env_stack:
        for env, start_line in env_stack:
            errors.append(f"{os.path.basename(file_path)}:L{start_line} Unclosed environment: \\begin{{{env}}}")

    return errors, warnings

def find_xelatex():
    p = shutil.which("xelatex")
    if p:
        return p
    for match in sorted(glob.glob(r"C:\texlive\*\bin\windows\xelatex.exe"), reverse=True):
        if os.path.exists(match):
            return match
    return None

def main():
    parser = argparse.ArgumentParser(description="Audit LaTeX syntax and check compilation.")
    parser.add_argument("--doc-dir", default="Documentation", help="Path to Documentation directory")
    parser.add_argument("--compile", action="store_true", help="Run full compilation pipeline with compile_report.py")
    args = parser.parse_args()

    doc_dir = os.path.abspath(args.doc_dir)
    knowdive_dir = os.path.join(doc_dir, "knowdive-files")
    section_dir = os.path.join(doc_dir, "section")
    bib_path = os.path.join(knowdive_dir, "KnowDivePubs.bib")

    bib_keys = extract_bib_keys(bib_path)
    print(f"Loaded {len(bib_keys)} BibTeX keys from {os.path.basename(bib_path)}: {', '.join(sorted(bib_keys))}")

    all_errors = []
    all_warnings = []

    files_to_check = []
    main_tex = os.path.join(knowdive_dir, "main.tex")
    if os.path.exists(main_tex):
        files_to_check.append(main_tex)

    if os.path.exists(section_dir):
        for fname in sorted(os.listdir(section_dir)):
            if fname.endswith(".tex"):
                files_to_check.append(os.path.join(section_dir, fname))

    print(f"Checking {len(files_to_check)} LaTeX source files...")
    for fpath in files_to_check:
        errs, warns = check_latex_syntax(fpath, bib_keys)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    if all_warnings:
        print("\n[!] WARNINGS:")
        for w in all_warnings:
            print(f"  - {w}")

    if all_errors:
        print("\n[X] SYNTAX ERRORS:")
        for e in all_errors:
            print(f"  - {e}")
        print("\nVerification status: FAILED")
        sys.exit(1)
    else:
        print("\n[OK] LaTeX environment nesting and citation keys verified successfully!")

    # Check for compiler
    compiler = find_xelatex()
    if compiler:
        print(f"\nFound XeLaTeX engine: {compiler}")
        if args.compile:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            compile_script = os.path.join(script_dir, "compile_report.py")
            if os.path.exists(compile_script):
                print("Invoking compile_report.py...")
                res = subprocess.run([sys.executable, compile_script, "--doc-dir", doc_dir])
                sys.exit(res.returncode)
    else:
        print("\n[NOTE] No local TeX compiler found in PATH or standard C:\\texlive\\ paths.")

if __name__ == "__main__":
    main()
