#!/usr/bin/env python3
"""
compile_report.py

Automates the complete LaTeX build pipeline for the KnowDive / DataScientia report:
1. Automatically discovers TeX Live executables (xelatex, bibtex) even if not yet on PATH.
2. Configures TEXINPUTS, BIBINPUTS, and BSTINPUTS to resolve knowdive-files and section paths.
3. Executes multi-pass compilation: xelatex -> bibtex -> xelatex -> xelatex.
4. Reports the compiled PDF location and page count.

Usage:
    python compile_report.py [--doc-dir PATH] [--clean]
"""

import os
import sys
import glob
import shutil
import argparse
import subprocess

def find_tex_binary(name):
    # 1. Check PATH
    p = shutil.which(name)
    if p:
        return p

    # 2. Check standard Windows TeX Live paths
    patterns = [
        r"C:\texlive\*\bin\windows",
        r"C:\Program Files\MiKTeX\miktex\bin\x64",
        r"C:\Program Files\texlive\*\bin\windows"
    ]
    for pattern in patterns:
        for match in sorted(glob.glob(pattern), reverse=True):
            cand = os.path.join(match, f"{name}.exe")
            if os.path.exists(cand):
                return cand
    return None

def main():
    parser = argparse.ArgumentParser(description="Compile the KnowDive LaTeX report using XeLaTeX.")
    parser.add_argument("--doc-dir", default="Documentation", help="Path to Documentation directory")
    parser.add_argument("--clean", action="store_true", help="Remove auxiliary files after build")
    args = parser.parse_args()

    doc_dir = os.path.abspath(args.doc_dir)
    knowdive_dir = os.path.join(doc_dir, "knowdive-files")
    main_tex = "knowdive-files/main.tex"

    xelatex_bin = find_tex_binary("xelatex")
    bibtex_bin = find_tex_binary("bibtex")

    if not xelatex_bin:
        print("[X] ERROR: xelatex executable not found on PATH or in C:\\texlive\\", file=sys.stderr)
        print("    Please ensure TeX Live is installed with XeTeX support.", file=sys.stderr)
        sys.exit(1)

    print(f"Found XeLaTeX : {xelatex_bin}")
    print(f"Found BibTeX  : {bibtex_bin or 'Not found (citations will not resolve)'}")
    print(f"Working Dir   : {doc_dir}")

    # Setup environment paths so XeLaTeX and BibTeX find all files seamlessly
    env = os.environ.copy()
    sep = ";" if os.name == "nt" else ":"
    env["TEXINPUTS"] = f"{knowdive_dir}{sep}{doc_dir}{sep}{sep}"
    env["BIBINPUTS"] = f"{knowdive_dir}{sep}{sep}"
    env["BSTINPUTS"] = f"{knowdive_dir}{sep}{sep}"

    # Step 1: Initial xelatex pass
    print("\n--- Pass 1: Initial XeLaTeX compilation ---")
    cmd_pass1 = [xelatex_bin, "-interaction=nonstopmode", main_tex]
    res1 = subprocess.run(cmd_pass1, cwd=doc_dir, env=env, capture_output=True, text=True)

    # Step 2: BibTeX pass if bibtex exists
    if bibtex_bin:
        print("--- Pass 2: BibTeX compilation ---")
        cmd_bib = [bibtex_bin, "main"]
        subprocess.run(cmd_bib, cwd=doc_dir, env=env, capture_output=True, text=True)

    # Step 3: Second xelatex pass to incorporate citations
    print("--- Pass 3: Second XeLaTeX pass (cross-references) ---")
    subprocess.run(cmd_pass1, cwd=doc_dir, env=env, capture_output=True, text=True)

    # Step 4: Final xelatex pass for LastPage and page numbers
    print("--- Pass 4: Final XeLaTeX pass (table of contents & page count) ---")
    res_final = subprocess.run(cmd_pass1, cwd=doc_dir, env=env, capture_output=True, text=True)

    pdf_path = os.path.join(doc_dir, "main.pdf")
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"\n[OK] Compilation SUCCEEDED!")
        print(f"PDF Output: {pdf_path} ({size_kb:.1f} KB)")
    else:
        print(f"\n[X] Compilation FAILED. Check main.log in {doc_dir}", file=sys.stderr)
        sys.exit(1)

    if args.clean:
        print("Cleaning auxiliary files...")
        aux_exts = [".aux", ".bbl", ".blg", ".log", ".out", ".toc", "texput.log"]
        for ext in aux_exts:
            for f in glob.glob(os.path.join(doc_dir, f"*{ext}")):
                try:
                    os.remove(f)
                except OSError:
                    pass
            for f in glob.glob(os.path.join(knowdive_dir, f"*{ext}")):
                try:
                    os.remove(f)
                except OSError:
                    pass
        print("Auxiliary files cleaned.")

if __name__ == "__main__":
    main()
