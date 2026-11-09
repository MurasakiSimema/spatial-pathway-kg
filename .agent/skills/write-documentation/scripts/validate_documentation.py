#!/usr/bin/env python3
"""
validate_documentation.py

Audits the LaTeX documentation in Documentation/ for:
1. Presence of all required section files (S1-S9, secA-Appendix, secB-Appendix).
2. Detection of unmodified template prompt text from Template_KG2026_report-pdf.pdf.
3. Violation of scientific and methodological cautions (forbidden phrasing from AGENT.md).
4. Completion of the Appendix A LLM questionnaire across all 6 phases.
5. Verification of main.tex metadata (title, author, revision history).

Usage:
    python validate_documentation.py [--doc-dir PATH]
"""

import os
import sys
import re
import argparse

# Key template prompt phrases from Template_KG2026_report-pdf.pdf that must be replaced
TEMPLATE_PHRASES = [
    "This section has to report and describe:",
    "First, we do the Purpose formalization which has to report",
    "How many scenarios initially considered?",
    "How many users initially considered?",
    "How many CQs initially considered?",
    "How many etypes terms initially considered?",
    "How many object property terms initially considered?",
    "How many data property terms initially considered?",
    "Answer phase specific LLM questionnaire in the appendix A",
    "Did you have to return to change something in the Purpose Definition",
    "How many entities initially considered?",
    "Other details/ difficulties encountered during Entity Definition via Karma",
    "Did the project respect the scheduling expected in the beginning ?",
    "Are the final results able to satisfy the initial Purpose ?",
    "which are the issues remained open at the end of the project ?"
]

# Forbidden scientific phrasing from AGENT.md Section 14
FORBIDDEN_PHRASES = [
    (re.compile(r"pathway\s+is\s+active\s+in", re.IGNORECASE), "Claiming pathway is active in cell type"),
    (re.compile(r"proves?\s+cell\s+presence", re.IGNORECASE), "Claiming proof of cell presence"),
    (re.compile(r"proves?\s+pathway\s+activation", re.IGNORECASE), "Claiming proof of pathway activation"),
    (re.compile(r"causes?\s+(this\s+)?cell\s+state", re.IGNORECASE), "Asserting causal cell state relationship"),
    (re.compile(r"proves?\s+cell\s+identity", re.IGNORECASE), "Claiming proof of cell identity from markers"),
    (re.compile(r"present\s+at\s+the\s+tissue\s+frontier", re.IGNORECASE), "Claiming cell presence at tissue frontier without spatial data")
]

REQUIRED_SECTIONS = [
    "S1.tex", "S2.tex", "S3.tex", "S4.tex", "S5.tex",
    "S6.tex", "S7.tex", "S8.tex", "S9.tex",
    "secA-Appendix.tex", "secB-Appendix.tex"
]

def check_main_tex(knowdive_dir):
    errors = []
    warnings = []
    main_path = os.path.join(knowdive_dir, "main.tex")
    if not os.path.exists(main_path):
        errors.append(f"Missing master file: {main_path}")
        return errors, warnings

    with open(main_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if "Author1, ..., AuthorN" in content:
        warnings.append("main.tex contains placeholder authors 'Author1, ..., AuthorN'")
    if "\\title{DataScientia KG Report Template}" in content:
        warnings.append("main.tex contains placeholder title 'DataScientia KG Report Template'")
    if "\\revision{0.3}{30.10.2026}{Mayukh Bagchi}{KG - 2026 - Project Report Template}" in content and "\\revision{1.0}" not in content:
        warnings.append("main.tex has not added a new revision entry for this project")

    return errors, warnings

def check_sections(section_dir):
    errors = []
    warnings = []

    for sec in REQUIRED_SECTIONS:
        sec_path = os.path.join(section_dir, sec)
        if not os.path.exists(sec_path):
            errors.append(f"Missing section file: {sec_path}")
            continue

        with open(sec_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

        if len(text.strip()) < 50:
            warnings.append(f"{sec} is nearly empty ({len(text.strip())} characters)")

        # Check for unedited template phrases
        for phrase in TEMPLATE_PHRASES:
            if phrase in text:
                warnings.append(f"{sec} contains unedited template prompt instruction: '{phrase}'")

        # Check for forbidden scientific phrases
        for pattern, reason in FORBIDDEN_PHRASES:
            match = pattern.search(text)
            if match:
                errors.append(f"{sec} violates AGENT.md scientific caution: {reason} (matched: '{match.group(0)}')")

    return errors, warnings

def check_appendix_a(section_dir):
    errors = []
    warnings = []
    secA_path = os.path.join(section_dir, "secA-Appendix.tex")
    if not os.path.exists(secA_path):
        return errors, warnings

    with open(secA_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    # Verify that the questions are not just the blank survey prompts
    # If CFS answers (e.g. "Never", "Rarely", "Often", "Always") are not selected or filled in:
    cfs_ratings_found = len(re.findall(r"\b(Never|Rarely|Sometimes|Often|Always)\b", text))
    # In the raw template, there are ~35 mentions in the scales themselves. A completed questionnaire will have > 70 mentions.
    if cfs_ratings_found < 60:
        warnings.append(f"Appendix A appears incomplete: only {cfs_ratings_found} CFS rating mentions found across 6 phases")

    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Audit LaTeX documentation.")
    parser.add_argument("--doc-dir", default="Documentation", help="Path to Documentation directory")
    args = parser.parse_args()

    doc_dir = os.path.abspath(args.doc_dir)
    knowdive_dir = os.path.join(doc_dir, "knowdive-files")
    section_dir = os.path.join(doc_dir, "section")

    print("=" * 70)
    print("Documentation Audit: Spatial Transcriptomics Knowledge Graph")
    print(f"Target Directory: {doc_dir}")
    print("=" * 70)

    all_errors = []
    all_warnings = []

    # 1. Main TeX
    e, w = check_main_tex(knowdive_dir)
    all_errors.extend(e)
    all_warnings.extend(w)

    # 2. Sections S1-S9 & Appendix B
    e, w = check_sections(section_dir)
    all_errors.extend(e)
    all_warnings.extend(w)

    # 3. Appendix A
    e, w = check_appendix_a(section_dir)
    all_errors.extend(e)
    all_warnings.extend(w)

    # Report results
    if all_warnings:
        print("\n[!] WARNINGS (Pending completion or unedited template text):")
        for w in all_warnings:
            print(f"  - {w}")

    if all_errors:
        print("\n[X] ERRORS (Violations of AGENT.md or missing critical files):")
        for err in all_errors:
            print(f"  - {err}")
        print("\nAudit status: FAILED (Resolve errors before final submission)")
        sys.exit(1)
    elif all_warnings:
        print("\nAudit status: PENDING (Resolve template text before finalizing report)")
        sys.exit(0)
    else:
        print("\n[OK] All documentation checks PASSED cleanly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
